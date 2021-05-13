# -*- coding: utf-8 -*-

from odoo import models, fields


class FiscalType(models.Model):
    _name = 'customer_infos.fiscal_type'
    _description = 'Fiscal Type'

    name = fields.Char(string='Fiscal Type', required=True, index=True)
