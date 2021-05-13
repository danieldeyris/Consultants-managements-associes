# -*- coding: utf-8 -*-

from odoo import models, fields


class LegalType(models.Model):
    _name = 'customer_infos.legal_type'
    _description = 'Legal Type'

    name = fields.Char(string='Legal Type', required=True, index=True)
