# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, tools, SUPERUSER_ID, _


class Task(models.Model):
    _inherit = "project.task"

    jonction_code = fields.Char(related='partner_id.jonction_code', store=True, readonly=True)
