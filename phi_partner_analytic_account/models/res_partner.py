# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    account_analytic_id = fields.Many2one('account.analytic.account', string='Compte Analytique')

    def get_account_analytic(self):
        return self.account_analytic_id or self.commercial_partner_id.account_analytic_id
