from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    millesime = fields.Many2one("abei_millesime.millesime")

    def _prepare_invoice(self):
        res = super()._prepare_invoice()
        res['millesime'] = self.millesime
        return res
