# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields

class Users(models.Model):
    _inherit = 'res.users'

    account_analytic_id = fields.Many2one('account.analytic.account', string='Compte Analytique')

