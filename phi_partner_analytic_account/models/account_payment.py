# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    account_analytic_id = fields.Many2one('account.analytic.account', string='Compte Analytique', store=True)

    @api.onchange('partner_id', 'invoice_ids')
    def _onchange_partner_id(self):
        values = {}
        if len(self.invoice_ids) == 1:
            values['account_analytic_id'] = self.invoice_ids[0].account_analytic_id
        if len(self.invoice_ids) > 1:
            account_analytic_id = False
            for invoice in self.invoice_ids:
                if not account_analytic_id:
                    account_analytic_id = invoice.account_analytic_id
                else:
                    if account_analytic_id != invoice.account_analytic_id:
                        account_analytic_id = False
                        break
            if account_analytic_id:
                values['account_analytic_id'] = account_analytic_id
        if self.partner_id and 'account_analytic_id' not in values:
            values['account_analytic_id'] = self.partner_id.get_account_analytic()
        if len(values):
            self.update(values)


class AccountBatchPayment(models.Model):
    _inherit = 'account.batch.payment'

    account_analytic_id = fields.Many2one('account.analytic.account', string='Compte Analytique', store=True)


class AccountPaymentRegister(models.TransientModel):
    _inherit = 'account.payment.register'

    account_analytic_id = fields.Many2one('account.analytic.account', string='Compte Analytique', store=True)

    @api.model
    def default_get(self, fields):
        rec = super(AccountPaymentRegister, self).default_get(fields)
        active_ids = self._context.get('active_ids')
        if not active_ids:
            return rec
        invoices = self.env['account.move'].browse(active_ids)
        account_analytic_id = False
        for invoice in invoices:
            if not account_analytic_id:
                account_analytic_id = invoice.account_analytic_id
            else:
                if account_analytic_id != invoice.account_analytic_id:
                    account_analytic_id = False
                    break
        if account_analytic_id:
            if 'account_analytic_id' not in rec:
                rec['account_analytic_id'] = account_analytic_id.id
        return rec

    def _prepare_payment_vals(self, invoices):
        values = super(AccountPaymentRegister, self)._prepare_payment_vals(invoices)
        if 'account_analytic_id' not in values:
            values['account_analytic_id'] = self.account_analytic_id.id
        return values
