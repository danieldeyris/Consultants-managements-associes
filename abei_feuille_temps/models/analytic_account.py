from odoo import models, fields, api, exceptions
from datetime import datetime


class AnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    partner_id = fields.Many2one('res.partner', check_company=True, required=True)
    nombre_bulletins = fields.Integer(string="Nombre bulletins")
    nombre_bulletins_old_value = fields.Integer()
    timesheet_quantity = fields.Boolean(compute="_compute_timesheet_quantity")

    @api.depends('task_id')
    def _compute_timesheet_quantity(self):
        for record in self:
            record.timesheet_quantity = record.task_id.sale_line_id.product_id.product_tmpl_id.timesheet_quantity

    @api.model
    def create(self, values):
        res = super().create(values)
        if not self.env.context.get('from_saisie_auto'):
            saisie_quantite_requise = self.env['project.task'].browse(values['task_id']).sale_line_id.product_id.product_tmpl_id.timesheet_quantity

            if saisie_quantite_requise and values['nombre_bulletins'] == 0:
                raise exceptions.UserError(
                    f"Saisie de quantité de bulletins necessaire pour cette tâche.")

            for record in res:
                # SI PRESENCE DE BULLETIN DANS LA LIGNE, FACTURATION
                if record.nombre_bulletins > 0:
                    # PARCOURS DU DEVIS POUR TROUVER LA LIGNE DE BULLETIN DE SALAIRE
                    order = record.task_id.sale_order_id
                    if order.id:
                        # PARCORUS DE TOUTES LES ORDER LINES
                        for ol in order.order_line:
                            # RECHERCHE D'UN ARTICLE DE TYPE BULLETIN DE SALAIRE
                            if ol.product_id.type_bulletin_de_salaire:
                                # VERIFICATION SI LE BULLETIN DE SALAIRE EST DE TYPE ABONNEMENT OU NON
                                # SI C'EST UNE BULLETIN DE SALAIRE A ABONNEMENT, VERIFICATION DANS L'ABONNEMENT
                                if ol.product_id.recurring_invoice:
                                    # PARCOURS DE TOUS LES ARTICLES PRESENT DANS LABONNEMENT
                                    for article_abonnement in ol.subscription_id.recurring_invoice_line_ids.product_id:
                                        # SI ARTICLE EN COURS DE VERIFICATION DANS L'ABONNEMENT = ARTICLE DU DEVIS
                                        if article_abonnement == ol.product_id:
                                            # SI QUANTITE SAISIE LORS DE LA SAISIE DE TEMPS DIFFERENTE DANS L'ABONNEMENT, ALORS CHANGEMENT QUANTITE DANS L'ABONNEMENT. SINON, RIEN
                                            if values['nombre_bulletins'] != ol.subscription_id.recurring_invoice_line_ids['quantity']:
                                                ol.subscription_id.recurring_invoice_line_ids['quantity'] = values['nombre_bulletins']

                                else: # SI C'EST UNE BULLETIN DE SALAIRE HORS ABONNEMENT, VERIFICATION DANS LE DEVIS
                                    ol['qty_delivered'] += values['nombre_bulletins']
                                break
                    else:
                        raise exceptions.UserError(f"La tâche n'est rattachée à aucun devis. Les bulletins ne sont pas facturables.")
                res['nombre_bulletins_old_value'] = values['nombre_bulletins']
        return res

    def write(self, vals):
        res = super().write(vals)
        # NOMBRE DE BULLETINS CHANGE DANS LA LIGNE DE SAISIE DE TEMPS ==> MISE A JOUR DU DEVIS CLIENT
        if 'nombre_bulletins' in vals:
            ligne_existante = False
            # PARCOURS DU DEVIS POUR TROUVER LA LIGNE DE BULLETIN DE SALAIRE
            order = self.task_id.sale_order_id
            if order.id:
                # PARCORUS DE TOUTES LES ORDER LINES
                for ol in order.order_line:
                    # RECHERCHE D'UN ARTICLE DE TYPE BULLETIN DE SALAIRE
                    if ol.product_id.type_bulletin_de_salaire:
                        # VERIFICATION SI LE BULLETIN DE SALAIRE EST DE TYPE ABONNEMENT OU NON
                        # SI C'EST UNE BULLETIN DE SALAIRE A ABONNEMENT, VERIFICATION DANS L'ABONNEMENT
                        if ol.product_id.recurring_invoice:
                            # PARCOURS DE TOUS LES ARTICLES PRESENT DANS LABONNEMENT
                            for article_abonnement in ol.subscription_id.recurring_invoice_line_ids.product_id:
                                # SI ARTICLE EN COURS DE VERIFICATION DANS L'ABONNEMENT = ARTICLE DU DEVIS
                                if article_abonnement == ol.product_id:
                                    # SI QUANTITE SAISIE LORS DE LA SAISIE DE TEMPS DIFFERENTE DANS L'ABONNEMENT, ALORS CHANGEMENT QUANTITE DANS L'ABONNEMENT. SINON, RIEN
                                    if vals['nombre_bulletins'] != ol.subscription_id.recurring_invoice_line_ids['quantity']:
                                        ol.subscription_id.recurring_invoice_line_ids['quantity'] = vals['nombre_bulletins']
                                        self.nombre_bulletins_old_value = vals['nombre_bulletins']

                        else:  # SI C'EST UNE BULLETIN DE SALAIRE HORS ABONNEMENT, VERIFICATION DANS LE DEVIS
                            ol['qty_delivered'] += (vals['nombre_bulletins']-self.nombre_bulletins_old_value)
                            self.nombre_bulletins_old_value = vals['nombre_bulletins']
                        break
        return res


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    ligne_saisie_temps_id = fields.Integer()


class Task(models.Model):
    _inherit = "project.task"

    ajouter_temps = fields.Float(string="Ajouter temps", store=False, default=0.0)
    ajouter_quantite = fields.Integer(string="Ajouter quantité", store=False, default=0)

    timesheet_quantity = fields.Boolean(compute="_compute_timesheet_quantity")

    # READONLY DE L'AJOUT DE QUANTITE SI ARTICLE DE LA TACHE PAS ELIGIBLE
    def _compute_timesheet_quantity(self):
        for record in self:
            record.timesheet_quantity = record.sale_line_id.product_id.product_tmpl_id.timesheet_quantity

    # AJOUT D'UNE LIGNE DE TEMPS DEPUIS LE MENU LIST (Colonne ajouter temps)
    # AJOUT D'UNE LIGNE DE QUANTITE DEPUIS LE MENU LIST (Colonne ajouter quantité)
    def write(self, vals):
        res = super(Task, self).write(vals)
        for record in self:
            # CAS 1 "Seulement ajouter temps"
            if 'ajouter_temps' in vals and 'ajouter_quantite' not in vals:
                date_saisie = datetime.today().strftime("%Y-%m-%d")
                self.env['account.analytic.line'].create({
                    'name': '--Saisie automatique--',
                    'project_id': record.project_id.id,
                    'task_id': record.ids[0],
                    'unit_amount': vals['ajouter_temps'],
                    'user_id': record.env.uid,
                    'date': date_saisie,
                })
                self.env.user.notify_success(
                    message=f"Saisie de temps de <b>{vals['ajouter_temps']}</b> heures ajoutée.")

            # CAS 2 "Seulement ajouter quantités"
            if 'ajouter_quantite' in vals and 'ajouter_temps' not in vals:
                date_saisie = datetime.today().strftime("%Y-%m-%d")
                self.env['account.analytic.line'].create({
                    'name': '--Saisie automatique--',
                    'project_id': record.project_id.id,
                    'task_id': record.ids[0],
                    'nombre_bulletins_old_value': vals['ajouter_quantite'],
                    'nombre_bulletins': vals['ajouter_quantite'],
                    'user_id': record.env.uid,
                    'date': date_saisie,
                })
                self.env.user.notify_success(
                    message=f"Saisie de <b>{vals['ajouter_quantite']}</b> bulletins.")

            # CAS 3 "Les deux"
            if 'ajouter_quantite' in vals and 'ajouter_temps' in vals:
                date_saisie = datetime.today().strftime("%Y-%m-%d")
                self.env['account.analytic.line'].create({
                    'name': '--Saisie automatique--',
                    'project_id': record.project_id.id,
                    'task_id': record.ids[0],
                    'unit_amount': vals['ajouter_temps'],
                    'nombre_bulletins_old_value': vals['ajouter_quantite'],
                    'nombre_bulletins': vals['ajouter_quantite'],
                    'user_id': record.env.uid,
                    'date': date_saisie,
                })

                self.env.user.notify_success(
                    message=f"Saisie de temps de <b>{vals['ajouter_temps']}</b> heures ajoutée.")
                self.env.user.notify_success(
                    message=f"Saisie de <b>{vals['ajouter_quantite']}</b> bulletins.")
        return res


