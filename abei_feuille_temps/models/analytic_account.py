from odoo import models, fields, api, exceptions
from datetime import datetime


class AnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    partner_id = fields.Many2one('res.partner', check_company=True, required=True)
    nombre_bulletins = fields.Integer(string="Nombre bulletins")

    # -------
    timesheet_quantity = fields.Boolean(compute="_compute_timesheet_quantity")
    # project_id = fields.Many2one(readonly=True)

    @api.depends('task_id')
    def _compute_timesheet_quantity(self):
        for record in self:
            record.timesheet_quantity = record.task_id.sale_line_id.product_id.product_tmpl_id.timesheet_quantity

    # @api.depends('task_id', 'task_id.project_id')
    # def _compute_project_id(self):
    #     for line in self:
    #         line.project_id = line.task_id.project_id
    # ----------

    @api.model
    def create(self, values):
        res = super().create(values)
        for record in res:
            # SI PRESENCE DE BULLETIN DANS LA LIGNE, FACTURATION
            if record.nombre_bulletins > 0:
                product_id = self.env['product.template'].search([(
                    'name', '=', 'Bulletin de Salaire'
                )])
                order = record.task_id.sale_order_id
                if order.id:
                    taxes = product_id.taxes_id.filtered(lambda r: r.company_id == order.company_id)
                    mois_annee_now = datetime.today().strftime("%m/%Y")
                    self.env['sale.order.line'].create({
                        'name': "Bulletin de salaire " + mois_annee_now,
                        'price_unit': product_id.list_price,
                        'product_uom_qty': record.nombre_bulletins,
                        'order_id': order.id,
                        'product_id': product_id.id,
                        'tax_id': [(6, 0, taxes.ids)],
                        'qty_delivered': record.nombre_bulletins,
                        'ligne_saisie_temps_id': record.id,
                    })
                else:
                    raise exceptions.UserError(f"La tâche n'est rattachée à aucun devis. Les bulletins ne sont pas facturables.")
        return res

    def write(self, vals):
        res = super().write(vals)
        # NOMBRE DE BULLETINS CHANGE DANS LA LIGNE DE SAISIE DE TEMPS ==> MISE A JOUR DU DEVIS CLIENT
        if 'nombre_bulletins' in vals:
            order = self.task_id.sale_order_id
            for record in order:
                for order_line in record.order_line:
                    if order_line.ligne_saisie_temps_id == self.id:
                        order_line['product_uom_qty'] = vals['nombre_bulletins']
                        order_line['qty_delivered'] = vals['nombre_bulletins']
        return res


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    ligne_saisie_temps_id = fields.Integer()


class Task(models.Model):
    _inherit = "project.task"

    ajouter_temps = fields.Float(string="Ajouter temps", store=False, default=0.0)

    # AJOUT D'UNE LIGNE DE TEMPS DEPUIS LE MENU LIST (Colonne ajouter temps)
    def write(self, vals):
        res = super(Task, self).write(vals)
        for record in self:
            if 'ajouter_temps' in vals:
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
        return res


