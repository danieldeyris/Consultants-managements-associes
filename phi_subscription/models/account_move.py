from odoo import fields, models, api


class AccountMove(models.Model):
    _inherit = "account.move"

    subscription_id = fields.Many2one('sale.subscription')

    def create(self, vals_list):
        res = super().create(vals_list)
        if res.subscription_id:
            res.invoice_date = res.subscription_id.recurring_next_date
        return res

