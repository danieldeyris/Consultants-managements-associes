from odoo import models, fields


class Users(models.Model):
    _inherit = "res.users"

    signature_line = fields.One2many("abei_signature.signature.line", "signature_id", string=".")


class SignatureLine(models.Model):
    _name = "abei_signature.signature.line"
    _description = "Une ligne de signature."

    company_signature = fields.Many2one("res.company", required=True, string="Cabinet")
    signature = fields.Html(string="Signature d'email", default="", required=True)

    signature_id = fields.Many2one("res.users", required=True, ondelete='cascade')

