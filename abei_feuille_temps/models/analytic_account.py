from odoo import models, fields, api, exceptions
from datetime import datetime


class AnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    partner_id = fields.Many2one('res.partner', check_company=True, required=True)
    nombre_bulletins = fields.Integer(string="Nombre bulletins")
    timesheet_quantity = fields.Boolean(compute="_compute_timesheet_quantity")

    @api.depends('task_id')
    def _compute_timesheet_quantity(self):
        for record in self:
            record.timesheet_quantity = record.task_id.sale_line_id.product_id.product_tmpl_id.timesheet_quantity

    @api.model
    def create(self, values):
        res = super().create(values)
        if not self.env.context.get('from_saisie_auto'):
            if 'task_id' in values:
                saisie_quantite_requise = self.env['project.task'].browse(values['task_id']).sale_line_id.product_id.product_tmpl_id.timesheet_quantity

                # SI SAISIE QUANTITE OBLIGATOIRE POUR L'ARTICLE ET QUE SAISIE = 0. VERIFICATION SAISIE DEJA PRESENTE DANS LA TACHE. SI OUI, C'EST OK. SI NON, PAS OK.
                if saisie_quantite_requise and res['nombre_bulletins'] == 0:
                    somme_nombre_bulletins = 0
                    for ligne_temps in res['task_id'].timesheet_ids:
                        somme_nombre_bulletins += ligne_temps.nombre_bulletins
                    if somme_nombre_bulletins == 0:
                        raise exceptions.UserError(
                            f"Saisie de quantité de bulletins necessaire pour cette tâche.")

                for record in res:
                    # SI PRESENCE DE BULLETIN DANS LA LIGNE, FACTURATION
                    if record.nombre_bulletins > 0:
                        # PARCOURS DU DEVIS POUR TROUVER LA LIGNE DE BULLETIN DE SALAIRE
                        order = record.task_id.sale_order_id
                        if order.id:
                            # PARCOURS DE TOUTES LES ORDER LINES
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
                                                somme_nombre_bulletins_ligne_temps_tache = 0
                                                # parcours de toutes les lignes dans la tâche, pour récupérer le nombre de bulletins saisis
                                                for ligne_temps_tache in res['task_id'].timesheet_ids:
                                                    somme_nombre_bulletins_ligne_temps_tache += ligne_temps_tache.nombre_bulletins
                                                    ol.subscription_id.recurring_invoice_line_ids['quantity'] = somme_nombre_bulletins_ligne_temps_tache

                                    else: # SI C'EST UNE BULLETIN DE SALAIRE HORS ABONNEMENT, VERIFICATION DANS LE DEVIS
                                        somme_nombre_bulletins_ligne_temps_tache = 0
                                        # parcours de toutes les lignes dans la tâche, pour récupérer le nombre de bulletins saisis
                                        for ligne_temps_tache in res['task_id'].timesheet_ids:
                                            somme_nombre_bulletins_ligne_temps_tache += ligne_temps_tache.nombre_bulletins
                                            ol['qty_delivered'] = somme_nombre_bulletins_ligne_temps_tache
                                    break
                        else:
                            raise exceptions.UserError(f"La tâche n'est rattachée à aucun devis. Les bulletins ne sont pas facturables.")
        return res

    def write(self, vals):
        res = super().write(vals)
        # NOMBRE DE BULLETINS CHANGE DANS LA LIGNE DE SAISIE DE TEMPS ==> MISE A JOUR DU DEVIS CLIENT
        if 'nombre_bulletins' in vals:
            ligne_existante = False
            # PARCOURS DU DEVIS POUR TROUVER LA LIGNE DE BULLETIN DE SALAIRE
            order = self.task_id.sale_order_id
            if order.id:
                # PARCOURS DE TOUTES LES ORDER LINES
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
                                    somme_nombre_bulletins_ligne_temps_tache = 0
                                    # parcours de toutes les lignes dans la tâche, pour récupérer le nombre de bulletins saisis
                                    for ligne_temps_tache in self.task_id.timesheet_ids:
                                        somme_nombre_bulletins_ligne_temps_tache += ligne_temps_tache.nombre_bulletins
                                        ol.subscription_id.recurring_invoice_line_ids['quantity'] = somme_nombre_bulletins_ligne_temps_tache

                        else:  # SI C'EST UNE BULLETIN DE SALAIRE HORS ABONNEMENT, VERIFICATION DANS LE DEVIS
                            somme_nombre_bulletins_ligne_temps_tache = 0
                            # parcours de toutes les lignes dans la tâche, pour récupérer le nombre de bulletins saisis
                            for ligne_temps_tache in self.task_id.timesheet_ids:
                                somme_nombre_bulletins_ligne_temps_tache += ligne_temps_tache.nombre_bulletins
                                ol['qty_delivered'] = somme_nombre_bulletins_ligne_temps_tache
                        break
        return res

    # def unlink(self):
    #
    #     order = self.task_id.sale_order_id
    #     if order.id:
    #         # PARCOURS DE TOUTES LES ORDER LINES
    #         for ol in order.order_line:
    #             # RECHERCHE D'UN ARTICLE DE TYPE BULLETIN DE SALAIRE
    #             if ol.product_id.type_bulletin_de_salaire:
    #                 # VERIFICATION SI LE BULLETIN DE SALAIRE EST DE TYPE ABONNEMENT OU NON
    #                 # SI C'EST UNE BULLETIN DE SALAIRE A ABONNEMENT, VERIFICATION DANS L'ABONNEMENT
    #                 if ol.product_id.recurring_invoice:
    #                     # PARCOURS DE TOUS LES ARTICLES PRESENT DANS LABONNEMENT
    #                     for article_abonnement in ol.subscription_id.recurring_invoice_line_ids.product_id:
    #                         # SI ARTICLE EN COURS DE VERIFICATION DANS L'ABONNEMENT = ARTICLE DU DEVIS
    #                         if article_abonnement == ol.product_id:
    #                             somme_nombre_bulletins_ligne_temps_tache = 0
    #                             # parcours de toutes les lignes dans la tâche, pour récupérer le nombre de bulletins saisis
    #                             for ligne_temps_tache in self.task_id.timesheet_ids:
    #                                 somme_nombre_bulletins_ligne_temps_tache += ligne_temps_tache.nombre_bulletins
    #                                 ol.subscription_id.recurring_invoice_line_ids[
    #                                     'quantity'] = somme_nombre_bulletins_ligne_temps_tache
    #
    #                 else:  # SI C'EST UNE BULLETIN DE SALAIRE HORS ABONNEMENT, VERIFICATION DANS LE DEVIS
    #                     somme_nombre_bulletins_ligne_temps_tache = 0
    #                     # parcours de toutes les lignes dans la tâche, pour récupérer le nombre de bulletins saisis
    #                     for ligne_temps_tache in self.task_id.timesheet_ids:
    #                         somme_nombre_bulletins_ligne_temps_tache += ligne_temps_tache.nombre_bulletins
    #                         ol['qty_delivered'] = somme_nombre_bulletins_ligne_temps_tache
    #                 break
    #     return super(AnalyticLine, self).unlink()


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
                    'nombre_bulletins': vals['ajouter_quantite'],
                    'user_id': record.env.uid,
                    'date': date_saisie,
                })

                self.env.user.notify_success(
                    message=f"Saisie de temps de <b>{vals['ajouter_temps']}</b> heures ajoutée.")
                self.env.user.notify_success(
                    message=f"Saisie de <b>{vals['ajouter_quantite']}</b> bulletins.")
        return res


