from odoo import fields, models, api


class SaleSubscription(models.Model):
    _inherit = "sale.subscription"

    # generate_recurring_invoice -->
    # action_subscription_invoice
    # _recurring_create_invoice
    def _recurring_create_invoice(self):
        super()._recurring_create_invoice()
        # return invoices

