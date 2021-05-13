# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.model
    def default_get(self, fields_list):
        result = super(SaleOrder, self).default_get(fields_list)
        if 'analytic_account_id' in fields_list and not result.get('analytic_account_id'):
            if result.get('partner_id'):
                result['analytic_account_id'] = self.env['res.partner'].browse(result['partner_id']).get_account_analytic().id
            if not result.get('analytic_account_id'):
                result['analytic_account_id'] = self.env.user.account_analytic_id.id

        return result

    analytic_account_id = fields.Many2one(copy=True)

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        values = {}
        values['analytic_account_id'] = self.partner_id.get_account_analytic()  or self.env.user.account_analytic_id.id
        self.update(values)

    def _prepare_invoice(self):
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        invoice_vals['account_analytic_id'] = self.analytic_account_id
        return invoice_vals

    @api.model
    def create(self, vals):
        if not vals.get('analytic_account_id') and vals.get('partner_id'):
                vals['analytic_account_id'] = self.env['res.partner'].browse(vals['partner_id']).get_account_analytic().id

        return super(SaleOrder, self).create(vals)
