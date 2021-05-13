# -*- coding: utf-8 -*-

from odoo import models, fields


class SocialType(models.Model):
    _name = 'customer_infos.social_type'
    _description = 'Social Type'

    name = fields.Char(string='Social Type', required=True, index=True)
