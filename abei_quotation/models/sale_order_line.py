from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    collaborateur = fields.Many2one('hr.employee',string="Collaborateur")

    @api.onchange('collaborateur')
    def _calcul_prix_collaborateur(self):
        for record in self:
            record.price_unit = record.collaborateur.taux_facturation
