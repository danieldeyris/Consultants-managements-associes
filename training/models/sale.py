from odoo import models,fields


class SaleOrder(models.Model):
    _inherit = "sale.order"

    name = fields.Char(string="Nom")
    number_order = fields.Integer(string="Nombre commandé")

    def _action_confirm(self):
        res = super()._action_confirm()
        for record in self:
            record.number_order = 5
        return res