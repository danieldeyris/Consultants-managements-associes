# -*- coding: utf-8 -*-

from odoo import models, fields


class SocialRegime(models.Model):
    _name = 'customer_infos.social_regime'
    _description = 'Social Regime'

    name = fields.Char(string='Social Regime', required=True, index=True)
