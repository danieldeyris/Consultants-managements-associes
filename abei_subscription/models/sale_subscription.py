from dateutil.relativedelta import relativedelta

from odoo import fields, models, _
from odoo.tools import format_date


class SaleSubscription(models.Model):
    _inherit = "sale.subscription"

    last_invoiced_date = fields.Date(copy=False)

    def _prepare_invoice_data(self):
        res = super()._prepare_invoice_data()
        res['subscription_id'] = self.id
        next_date = self.last_invoiced_date or self.date_start
        res['invoice_date_due'] = next_date
        recurring_next_date = self._get_recurring_next_date(self.recurring_rule_type, self.recurring_interval, next_date, next_date.day)
        self.last_invoiced_date = fields.Date.from_string(recurring_next_date)
        end_date = self.last_invoiced_date - relativedelta(days=1)
        res['narration'] = _("This invoice covers the following period: %s - %s") % (format_date(self.env, next_date), format_date(self.env, end_date))
        return res
