from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    # réseaux
    facebook = fields.Char(string="Facebook")
    linkedin = fields.Char(string="Linkedin")
    twitter = fields.Char(string="Twitter")
