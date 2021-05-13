# -*- coding: utf-8 -*-

from odoo import models, fields


class VatType(models.Model):
    _name = 'customer_infos.vat_type'
    _description = 'Vat Type'

    name = fields.Char(string='Vat Type', required=True, index=True)
