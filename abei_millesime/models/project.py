# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class Task(models.Model):
    _inherit = "project.task"

    millesime_id = fields.Many2one('abei_millesime.millesime', string='Millesime')
