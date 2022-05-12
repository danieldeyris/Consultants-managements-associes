from odoo import models, fields


class AnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    client = fields.Many2one('res.partner', string="Client", required=True, domain=['|', ('is_company', '=', True), ('parent_id', '=', False)])
