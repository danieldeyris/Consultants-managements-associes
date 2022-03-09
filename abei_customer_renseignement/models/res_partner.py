from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    # Renseignements
    telephone_domicile = fields.Char(string="Téléphone domicile")
    telephone_perso = fields.Char(string="Téléphone perso")
    regime_fiscal_perso = fields.Many2one('customer_infos.fiscal_type', string="Régime Fiscal Perso")
    regime_social_perso = fields.Many2one('customer_infos.social_type', string="Régime Social Perso")
    facebook_perso = fields.Char(string="Facebook Perso")
    linkedin_perso = fields.Char(string="Linkedin Perso")
    twitter_perso = fields.Char(string="Twitter Perso")

