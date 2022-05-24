from odoo import fields, models, api


class AccountMove(models.Model):
    _inherit = "account.move"

    millesime = fields.Many2one("abei_millesime.millesime", readonly=True)
