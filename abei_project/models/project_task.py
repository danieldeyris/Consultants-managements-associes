from odoo import fields, models, api, exceptions, _
from datetime import datetime


class Task(models.Model):
    _inherit = "project.task"

    type_temps = fields.Many2one('abei_feuille_temps.type_temps', string="Type de saisie de temps", help="Permet de redéfinir le type de saisie de temps si différent de ceux de l'article.")
    temps_incompressible = fields.Float(string='Temps imcompressible')
    temps_unitaire = fields.Float(string='Temps unitaire par bulletin')
    quantite_bulletin_estime = fields.Float(string="Quantité bulletin estimé", help="La quantité indiquée à cet endroit permet d'aider à la saisie automatique de temps. (Temps unitaire * Quantité de bulletin estimée)")

    # LORS DE LA CREATION DE LA TACHE, RECUPERATION DU TYPE DE TEMPS DE L'ARTICLE
    @api.model
    def create(self, vals_list):
        self = self.with_context(from_create=True)
        res = super().create(vals_list)
        # SI TYPE DE TEMPS DEFINI POUR L'ARTCILE, RECUPERATION
        if res.sale_line_id.product_id.type_temps:
            res.type_temps = res.sale_line_id.product_id.type_temps
            res.temps_incompressible = res.sale_line_id.product_id.type_temps.temps_incompressible
            res.temps_unitaire = res.sale_line_id.product_id.type_temps.temps_unitaire
        # SI PRESENCE D'UN ARTICLE DE TYPE BULLETIN DE SALAIRE, RECUPERATION QUANTITE SAISIE
        if res.sale_line_id.product_id.name in ['Bulletin de Salaire','Bulletin de salaire']:
            res.quantite_bulletin_estime = res.sale_line_id.product_uom_qty
        res['tag_ids'] = res.sale_line_id.product_id.etiquette
        res['millesime_id'] = res.sale_line_id.order_id.millesime
        res['jonction_code'] = res.sale_line_id.order_id.partner_id.jonction_code
        res['user_id'] = res.sale_line_id.collaborateur.user_id
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

    # MODIFICATION APPORTEE A UNE TACHE
    def write(self, vals):
        res = super(Task, self).write(vals)
        if not self.env.context.get('from_create'):
            flag = False
            # RECUPERATION ETIQUETTE DE LA TACHE
            for etiquettes_tache_projet in self.project_id.etiquette_projet:
                # VERIFICATION ETIQUETTE UTILISATEUR CONNECTE POUR VERIFIER SON DROIT DE MODIFIER
                if etiquettes_tache_projet.name == self.env.user.employee_ids.department_id.name:
                    flag = True # CREATION FLAG MODIFICATION AUTORISEE
            # CAS PROJET N'AS PAS D'ETIQUETTE, MODIFICATION AUTORISEE POUR N'IMPORTE QUI
            if not self.project_id.etiquette_projet:
                flag = True

            # VERIFICATION TACHE ASSIGNEE A L'UTILISATEUR CONNECTE, BIEN QUE NE FAISANT PAS PARTIE DU DEPARTEMENT
            if self.user_id.id == self.env.uid:
                flag = True
            if not flag:
                raise exceptions.UserError(
                    f"Votre département métier '{self.env.user.employee_ids.department_id.name}' ne vous permet pas de modifier une tâche provenant d'un autre département métier.")
        return res

    @api.onchange('stage_id')
    def verification_changement_etape(self):
        # SI TACHE SELECTIONNE EST POSITIONNEE SUR UNE ETAPE DE CLOTURE :
        if self.stage_id.is_closed:
            saisie_effectuee = False
            # ALORS VERIFICATION NECESSISTE SAISIE
            for test in self.sale_line_id:
                # # SI ARTICLE DEFINI COMME 'saisie de temps obligatoire'
                # AUCUNE SAISIE DE TEMPS N'EST FAITE. VERIFICATION SI AJOUT AUTOMATIQUE DE TEMPS PAR LE SYSTEME
                if self.effective_hours == 0:
                    # SI TYPE DE TEMPS PREDEFINI, ALORS UTILISATION CE CES TEMPS POUR FAIRE LA SAISIE AUTOMATIQUE DE L'UTILISATEUR
                    if self.type_temps.id:
                        saisie_effectuee = True

                        # SAISIE DE TEMPS AUTOMATIQUE
                        # UTILISATION DES INFORMATIONS D'HEURES (potentiellement) REDEFIENIES DANS LA TACHE, PLUTOT QUE DE PRENDRE LES HEURES DE L'ARTICLE
                        calcul_temp_unitaire = self.quantite_bulletin_estime * self.temps_unitaire
                        nombre_heures = self.temps_incompressible + calcul_temp_unitaire
                        date_saisie = datetime.today().strftime("%Y-%m-%d")
                        self.env['account.analytic.line'].create({
                            'name': '--Saisie automatique clôture tâche--',
                            'project_id': self.project_id.id,
                            'task_id': self.ids[0],
                            'unit_amount': nombre_heures,
                            'user_id': self.env.uid,
                            'date': date_saisie,
                        })
                        # NOTIFICATION
                        self.env.user.notify_success(
                            message=f'<center>Tâche terminée.</center><br>Saisie automatique de <b>{nombre_heures}</b> heures.')

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

    def action_cloturer_tache(self):
        for record in self:
            # 1ere étape : Récupérer toutes les étapes du projet
            etapes = self.env['project.task.type'].search([('project_ids', '=', record.project_id.id)])
            for etape in etapes:
                # 2eme étape : Focus l'étape de clôture
                if etape.is_closed:
                    # Clôture de la tâche selectionnée
                    saisie_effectuee = False
                    transfert_autorise = True
                    # ALORS VERIFICATION NECESSISTE SAISIE
                    for test in record.sale_line_id:
                        # # SI ARTICLE DEFINI COMME 'saisie de temps obligatoire'
                        # AUCUNE SAISIE DE TEMPS N'EST FAITE. VERIFICATION SI AJOUT AUTOMATIQUE DE TEMPS PAR LE SYSTEME
                        if record.effective_hours == 0:
                            # SI TYPE DE TEMPS PREDEFINI, ALORS UTILISATION CE CES TEMPS POUR FAIRE LA SAISIE AUTOMATIQUE DE L'UTILISATEUR
                            if record.type_temps.id:
                                saisie_effectuee = True

                            # SI ARTICLE DEFINI COMME 'saisie de temps obligatoire'
                            if test.product_id.timesheet_mandatory and not saisie_effectuee:
                                transfert_autorise = False
                                # SINON , AVERTISSEMENT SAISIE NECESSAIRE
                                self.env.user.notify_danger(
                                    message=f"<CENTER><b><u>SAISIE DE TEMPS NECESSAIRE</u></b></CENTER> <br>L'étape <b>'{record.stage_id.name}'</b> est marquée comme étant une étape de clôture et l'article <b>'{test.product_id.name}'</b> comme nécessitant une saisie de temps obligatoire avant sa clôture. <br><br>Hors, votre tâche <b>'{record.name}'</b> ne comporte aucune saisie de temps. <br><br>Veuillez faire au moins une saisie de temps pour pouvoir cloturer votre tâche.")
                                break

                        # SI ARTICLE DEFINI COMME 'saisie de quantité obligatoire'
                        if test.product_id.timesheet_quantity:
                            somme_nombre_bulletins = 0
                            for ligne_temps in record.timesheet_ids:
                                somme_nombre_bulletins += ligne_temps.nombre_bulletins
                            if somme_nombre_bulletins == 0:
                                transfert_autorise = False
                                self.env.user.notify_danger(
                                    message=f"<CENTER><b><u>SAISIE QUANTITES BULLETINS NECESSAIRE</u></b></CENTER> <br>L'étape <b>'{record.stage_id.name}'</b> est marquée comme étant une étape de clôture et l'article <b>'{test.product_id.name}'</b> comme nécessitant la saisie de quantité de bulletins. <br><br>Hors, votre tâche <b>'{record.name}'</b> ne comporte aucune saisie de quantité de bulletins. <br><br>Veuillez faire au moins une saisie de quantité de bulletins pour pouvoir cloturer votre tâche.")
                                break

                        if transfert_autorise:
                            self.env['project.task'].browse(record.id).write({'stage_id': etape.id})
                            if record.effective_hours == 0:
                                # SAISIE DE TEMPS AUTOMATIQUE
                                # UTILISATION DES INFORMATIONS D'HEURES (potentiellement) REDEFIENIES DANS LA TACHE, PLUTOT QUE DE PRENDRE LES HEURES DE L'ARTICLE
                                calcul_temp_unitaire = record.quantite_bulletin_estime * record.temps_unitaire
                                nombre_heures = record.temps_incompressible + calcul_temp_unitaire
                                date_saisie = datetime.today().strftime("%Y-%m-%d")
                                self.env['account.analytic.line'].create({
                                    'name': '--Saisie automatique clôture tâche--',
                                    'project_id': record.project_id.id,
                                    'task_id': record.ids[0],
                                    'unit_amount': nombre_heures,
                                    'user_id': record.env.uid,
                                    'date': date_saisie,
                                })
                                # NOTIFICATION
                                self.env.user.notify_success(
                                    message=f'<center>Tâche terminée.</center><br>Saisie automatique de <b>{nombre_heures}</b> heures.')