# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    fiscal_type_id = fields.Many2one('customer_infos.fiscal_type', string='Fiscal Type')
    social_regime_id = fields.Many2one('customer_infos.social_regime', string='Social Regime')
    vat_type_id = fields.Many2one('customer_infos.vat_type', string='Vat Type')
    legal_type_id = fields.Many2one('customer_infos.legal_type', string='Legal Type')
    social_type_id = fields.Many2one('customer_infos.social_type', string='social Type')
    customer_activity_type_id = fields.Many2one('customer_infos.activity_type', string='Activity Type')
    naf_code = fields.Char(string='Code NAF')

