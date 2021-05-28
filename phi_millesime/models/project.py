# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, tools, SUPERUSER_ID, _


class Task(models.Model):
    _inherit = "project.task"

    millesime_id = fields.Many2one('phi_millesime.millesime', string='Millesime')
