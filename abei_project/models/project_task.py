from odoo import fields, models, api, exceptions, _
from datetime import datetime


class Task(models.Model):
    _inherit = "project.task"

    type_temps = fields.Many2one('abei_feuille_temps.type_temps', string="Type de saisie de temps")
    temps_incompressible = fields.Float(string='Temps imcompressible')
    temps_unitaire = fields.Float(string='Temps unitaire')

    # LORS DE LA CREATION DE LA TACHE, RECUPERATION DU TYPE DE TEMPS DE L'ARTICLE
    @api.model
    def create(self, vals_list):
        res = super().create(vals_list)
        if res.sale_line_id.product_id.type_temps:
            res.type_temps = res.sale_line_id.product_id.type_temps
            res.temps_incompressible = res.sale_line_id.product_id.type_temps.temps_incompressible
            res.temps_unitaire = res.sale_line_id.product_id.type_temps.temps_unitaire
        return res

    # CAS CHANGEMENT TYPE TEMPS -> REDEFINITION DES TEMPS AFFICHES
    @api.onchange('type_temps')
    def changement_type_temps(self):
        self.temps_incompressible = self.type_temps.temps_incompressible
        self.temps_unitaire = self.type_temps.temps_unitaire


    def create_notification(self):
        message = {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Warning!'),
                'message': 'You cannot do this action now',
                'sticky': False,
            }
        }
        return message

    @api.onchange('stage_id')
    def verification_changement_etape(self):
        saisie_effectuee = False
        # SI TACHE SELECTIONNE EST POSITIONNEE SUR UNE ETAPE DE CLOTURE :
        if self.stage_id.is_closed:
            # ALORS VERIFICATION NECESSISTE SAISIE
            for test in self.sale_line_id:
                # # SI ARTICLE DEFINI COMME 'saisie de temps obligatoire'
                # if test.product_id.timesheet_mandatory:
                # AUCUNE SAISIE DE TEMPS N'EST FAITE. VERIFICATION SI AJOUT AUTOMATIQUE DE TEMPS PAR LE SYSTEME
                if self.effective_hours == 0:
                    # SI TYPE DE TEMPS PREDEFINI, ALORS UTILISATION CE CES TEMPS POUR FAIRE LA SAISIE AUTOMATIQUE DE L'UTILISATEUR
                    print(self.type_temps.id)
                    if self.type_temps.id:
                        saisie_effectuee = True
                        # NOTIFICATION
                        self.create_notification() #NE MARCHE PAS

                        # SAISIE DE TEMPS AUTOMATIQUE
                        #nombre_heures = self.type_temps.temps_incompressible + self.type_temps.temps_unitaire
                        # UTILISATION DES INFORMATIONS D'HEURES (potentiellement) REDEFIENIES DANS LA TACHE, PLUTOT QUE DE PRENDRE LES HEURES DE L'ARTICLE
                        nombre_heures = self.temps_incompressible + self.temps_unitaire # TEMPS_UNITAIRE A REVOIR EN FONCTION DE LA REPONSE DE JEAN-MARIE
                        date_saisie = datetime.today().strftime("%Y-%m-%d")
                        self.env['account.analytic.line'].create({
                            'name': '--Saisie automatique--',
                            'project_id': self.project_id.id,
                            'task_id': self.ids[0],
                            'unit_amount': nombre_heures,
                            'user_id': self.env.uid,
                            'date': date_saisie,
                        })

                    # SI ARTICLE DEFINI COMME 'saisie de temps obligatoire'
                    if test.product_id.timesheet_mandatory and not saisie_effectuee:
                        # SINON , AVERTISSEMENT SAISIE NECESSAIRE
                        raise exceptions.UserError(
                            f"L'étape '{self.stage_id.name}' est marquée comme étant une étape de clôture et l'article '{test.product_id.name}' comme nécessitant une saisie de temps obligatoire avant sa clôture. \n\nHors, votre tâche '{self.name}' ne comporte aucune saisie de temps. \n\nVeuillez faire au moins une saisie de temps pour pouvoir cloturer votre tâche.")


                # SI ARTICLE DEFINI COMME 'saisie de quantité obligatoire'
                if test.product_id.timesheet_quantity:
                    somme_nombre_bulletins = 0
                    for ligne_temps in self.timesheet_ids:
                        somme_nombre_bulletins += ligne_temps.nombre_bulletins
                    if somme_nombre_bulletins == 0:
                        raise exceptions.UserError(
                            f"L'étape '{self.stage_id.name}' est marquée comme étant une étape de clôture et l'article '{test.product_id.name}' comme nécessitant la saisie de quantité de bulletins. \n\nHors, votre tâche '{self.name}' ne comporte aucune saisie de quantité de bulletins. \n\nVeuillez faire au moins une saisie de quantité de bulletins pour pouvoir cloturer votre tâche.")
