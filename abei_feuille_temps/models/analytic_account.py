from odoo import models, fields


class AnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    partner_id = fields.Many2one('res.partner', string='Client', check_company=True, required=True)

