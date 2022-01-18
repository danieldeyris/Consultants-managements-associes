# -*- coding: utf-8 -*-

from odoo import models, fields


class Millesime(models.Model):
    _name = 'phi_millesime.millesime'
    _description = 'Millesime'

    name = fields.Char(string='Millesime', required=True, index=True)
