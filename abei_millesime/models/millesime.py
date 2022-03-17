from odoo import models, fields


class Millesime(models.Model):
    _name = 'abei_millesime.millesime'
    _description = 'Millésime'

    name = fields.Char(string='Millesime', required=True, index=True)
    active = fields.Boolean(string="Actif", default=True)
