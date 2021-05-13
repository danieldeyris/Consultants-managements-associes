# -*- coding: utf-8 -*-

from odoo import models, fields


class ActivityType(models.Model):
    _name = 'customer_infos.activity_type'
    _description = 'Activity Type'

    name = fields.Char(string='Activity Type', required=True, index=True)
