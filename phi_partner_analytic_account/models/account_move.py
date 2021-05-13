# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _

class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.model
    def default_get(self, fields_list):
        result = super(AccountMove, self).default_get(fields_list)
        if 'account_analytic_id' in fields_list and not result.get('account_analytic_id'):
            if result.get('purchase_id'):
                result['account_analytic_id'] = self.env['purchase.order'].browse(result['purchase_id']).account_analytic_id.id
            elif result.get('partner_id'):
                result['account_analytic_id'] = self.env['res.partner'].browse(result['partner_id']).get_account_analytic().id
        return result

    account_analytic_id = fields.Many2one('account.analytic.account', string='Analytic Account', domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        values = {}
        if self.partner_id:
            values['account_analytic_id'] = self.partner_id.get_account_analytic()
            self.update(values)

    @api.model
    def create(self, vals):
        if not vals.get('account_analytic_id') and vals.get('reversed_entry_id'):
                vals['account_analytic_id'] = self.env['account.move'].browse(vals['reversed_entry_id']).account_analytic_id.id

        if not vals.get('account_analytic_id') and vals.get('purchase_id'):
                vals['account_analytic_id'] = self.env['purchase.order'].browse(vals['purchase_id']).account_analytic_id.id

        if not vals.get('account_analytic_id') and vals.get('payment_id'):
                vals['account_analytic_id'] = self.env['account.payment'].browse(vals['payment_id']).account_analytic_id.id

        if not vals.get('account_analytic_id') and vals.get('payment_id'):
                vals['account_analytic_id'] = self.env['account.payment'].browse(vals['payment_id']).account_analytic_id.id

        if not vals.get('account_analytic_id') and vals.get('partner_id'):
                vals['account_analytic_id'] = self.env['res.partner'].browse(vals['partner_id']).get_account_analytic().id

        return super(AccountMove, self).create(vals)


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    @api.onchange('account_id')
    def _onchange_account_id_phidias(self):
        for line in self:
            values = {}
            if line.move_id:
                values['analytic_account_id'] = line.move_id.account_analytic_id
                line.update(values)

    @api.model_create_multi
    def create(self, vals):
        for val in vals:
            if not val.get('analytic_account_id') and not val.get('display_type'):
                if val.get('move_id'):
                    val['analytic_account_id'] = self.env['account.move'].browse(val.get('move_id')).account_analytic_id.id

        return super(AccountMoveLine, self).create(vals)
