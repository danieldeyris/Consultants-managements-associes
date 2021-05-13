# -*- coding: utf-8 -*-
from odoo.tests.common import SavepointCase
import datetime


class TestSubscription(SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestSubscription, cls).setUpClass()
        # disable most emails for speed
        context_no_mail = {'no_reset_password': True, 'mail_create_nosubscribe': True, 'mail_create_nolog': True}

        # Minimal CoA & taxes setup
        user_type_payable = cls.env.ref('account.data_account_type_payable').with_context(context_no_mail)
        cls.account_payable = cls.env['account.account'].create({
            'code': 'NC1110',
            'name': 'Test Payable Account',
            'user_type_id': user_type_payable.id,
            'reconcile': True
        })
        user_type_receivable = cls.env.ref('account.data_account_type_receivable').with_context(context_no_mail)
        cls.account_receivable = cls.env['account.account'].create({
            'code': 'NC1111',
            'name': 'Test Receivable Account',
            'user_type_id': user_type_receivable.id,
            'reconcile': True
        })
        user_type_income = cls.env.ref('account.data_account_type_direct_costs').with_context(context_no_mail)
        cls.account_income = cls.env['account.account'].create({
            'code': 'NC1112', 'name':
            'Sale - Test Account',
            'user_type_id': user_type_income.id
        })

        Tax = cls.env['account.tax'].with_context(context_no_mail)
        cls.tax_10 = Tax.create({
            'name': "10% tax",
            'amount_type': 'percent',
            'amount': 10,
        })

        Journal = cls.env['account.journal'].with_context(context_no_mail)
        cls.journal = Journal.create({
            'name': 'Sales Journal',
            'type': 'sale',
            'code': 'SUB0',
        })

        # Test user
        TestUsersEnv = cls.env['res.users'].with_context({'no_reset_password': True})
        group_portal_id = cls.env.ref('base.group_portal').id
        cls.user_portal = TestUsersEnv.create({
            'name': 'Beatrice Portal',
            'login': 'Beatrice',
            'email': 'beatrice.employee@example.com',
            'groups_id': [(6, 0, [group_portal_id])],
            'property_account_payable_id': cls.account_payable.id,
            'property_account_receivable_id': cls.account_receivable.id,
        })

        # Test products
        ProductTmpl = cls.env['product.template'].with_context(context_no_mail)
        cls.product_tmpl_annual = ProductTmpl.create({
            'name': 'TestProductYear',
            'type': 'service',
            'subscription_product': True,
            'period': 'annual',
            'anticipation': 0,
            'uom_id': cls.env.ref('uom.product_uom_unit').id,
            'price': 200.00,
            'taxes_id': [(6, 0, [cls.tax_10.id])],
            'property_account_income_id': cls.account_income.id,
            'proportion': 'none',
        })

        cls.product_tmpl_bimonthly = ProductTmpl.create({
            'name': 'TestProductBimonthly',
            'type': 'service',
            'subscription_product': True,
            'period': 'bimonthly',
            'anticipation': 0,
            'uom_id': cls.env.ref('uom.product_uom_unit').id,
            'price': 200.0,
            'taxes_id': [(6, 0, [cls.tax_10.id])],
            'property_account_income_id': cls.account_income.id,
            'proportion': 'none',
        })

        cls.product_tmpl_weekly = ProductTmpl.create({
            'name': 'TestProductWeekly',
            'type': 'service',
            'subscription_product': True,
            'period': 'weekly',
            'anticipation': 0,
            'uom_id': cls.env.ref('uom.product_uom_unit').id,
            'price': 200.00,
            'taxes_id': [(6, 0, [cls.tax_10.id])],
            'property_account_income_id': cls.account_income.id,
            'proportion': 'none',
        })

        cls.product_tmpl_daily = ProductTmpl.create({
            'name': 'TestProductDaily',
            'type': 'service',
            'subscription_product': True,
            'period': 'daily',
            'anticipation': 0,
            'uom_id': cls.env.ref('uom.product_uom_unit').id,
            'price': 200.00,
            'taxes_id': [(6, 0, [cls.tax_10.id])],
            'property_account_income_id': cls.account_income.id,
            'proportion': 'none',
        })

        cls.product_tmpl_monthly = ProductTmpl.create({
            'name': 'TestProductMonthly',
            'type': 'service',
            'subscription_product': True,
            'period': 'monthly',
            'anticipation': 0,
            'uom_id': cls.env.ref('uom.product_uom_unit').id,
            'price': 200.00,
            'taxes_id': [(6, 0, [cls.tax_10.id])],
            'property_account_income_id': cls.account_income.id,
            'proportion': 'none',
        })

        cls.product_tmpl_semester = ProductTmpl.create({
            'name': 'TestProductsemester',
            'type': 'service',
            'subscription_product': True,
            'period': 'semester',
            'anticipation': 0,
            'uom_id': cls.env.ref('uom.product_uom_unit').id,
            'price': 200.00,
            'taxes_id': [(6, 0, [cls.tax_10.id])],
            'property_account_income_id': cls.account_income.id,
            'proportion': 'none',
        })

        cls.product_tmpl_quarter = ProductTmpl.create({
            'name': 'TestProductquarter',
            'type': 'service',
            'subscription_product': True,
            'period': 'quarter',
            'anticipation': 0,
            'uom_id': cls.env.ref('uom.product_uom_unit').id,
            'price': 200.00,
            'taxes_id': [(6, 0, [cls.tax_10.id])],
            'property_account_income_id': cls.account_income.id,
            'proportion': 'none',
        })

        # Subscription
        Subscription = cls.env['phi_subscription.subscription'].with_context(context_no_mail)

        cls.subscription_annual = Subscription.create({
            'name': 'SubscriptionYear',
            'partner_id': cls.user_portal.partner_id.id,
            'product_id': cls.product_tmpl_annual.product_variant_id.id,
            'date_start': datetime.date(2020, 1, 1),
        })

        cls.subscription_bimonthly = Subscription.create({
            'name': 'Subscriptionbimonthly',
            'partner_id': cls.user_portal.partner_id.id,
            'product_id': cls.product_tmpl_bimonthly.product_variant_id.id,
            'date_start': datetime.date(2020, 1, 1),
        })

        cls.subscription_weekly = Subscription.create({
            'name': 'Subscriptionweekly',
            'partner_id': cls.user_portal.partner_id.id,
            'product_id': cls.product_tmpl_weekly.product_variant_id.id,
            'date_start': datetime.date(2019, 12, 30),
        })

        cls.subscription_daily = Subscription.create({
            'name': 'Subscriptiondaily',
            'partner_id': cls.user_portal.partner_id.id,
            'product_id': cls.product_tmpl_daily.product_variant_id.id,
            'date_start': datetime.date(2020, 1, 1),
        })

        cls.subscription_monthly = Subscription.create({
            'name': 'Subscriptionmonthly',
            'partner_id': cls.user_portal.partner_id.id,
            'product_id': cls.product_tmpl_monthly.product_variant_id.id,
            'date_start': datetime.date(2020, 1, 1),
        })

        cls.subscription_semester = Subscription.create({
            'name': 'Subscriptionsemester',
            'partner_id': cls.user_portal.partner_id.id,
            'product_id': cls.product_tmpl_semester.product_variant_id.id,
            'date_start': datetime.date(2020, 1, 1),
        })

        cls.subscription_quarter = Subscription.create({
            'name': 'Subscriptionquarter',
            'partner_id': cls.user_portal.partner_id.id,
            'product_id': cls.product_tmpl_quarter.product_variant_id.id,
            'date_start': datetime.date(2020, 1, 1),
        })

        # subscription run
        SubscriptionRun = cls.env['phi_subscription.subscription_run'].with_context(context_no_mail)

        cls.subscription_run_2019_12_31 = SubscriptionRun.create({
            'name' : "End Date 31/12/2019",
            'date_end': datetime.date(2019, 12, 31),
            'partner_id': cls.user_portal.partner_id.id,
        })

        cls.subscription_run_2020_01_01 = SubscriptionRun.create({
            'name': "End Date 01/01/2020",
            'date_end': datetime.date(2020, 1, 1),
            'partner_id': cls.user_portal.partner_id.id,
        })

        cls.subscription_run_2020_01_06 = SubscriptionRun.create({
            'name': "End Date 06/01/2020",
            'date_end': datetime.date(2020, 1, 6),
            'partner_id': cls.user_portal.partner_id.id,
        })

        cls.subscription_run_2020_01_07 = SubscriptionRun.create({
            'name': "End Date 07/01/2020",
            'date_end': datetime.date(2020, 1, 7),
            'partner_id': cls.user_portal.partner_id.id,
        })

        cls.subscription_run_2020_01_14 = SubscriptionRun.create({
            'name': "End Date 14/01/2020",
            'date_end': datetime.date(2020, 1, 14),
            'partner_id': cls.user_portal.partner_id.id,
        })

        cls.subscription_run_2020_01_21 = SubscriptionRun.create({
            'name': "End Date 21/01/2020",
            'date_end': datetime.date(2020, 1, 21),
            'partner_id': cls.user_portal.partner_id.id,
        })

        cls.subscription_run_2020_01_31 = SubscriptionRun.create({
            'name': "End Date 31/01/2020",
            'date_end': datetime.date(2020, 1, 31),
            'partner_id': cls.user_portal.partner_id.id,
        })

        cls.subscription_run_2020_02_29 = SubscriptionRun.create({
            'name': "End Date 29/02/2020",
            'date_end': datetime.date(2020, 2, 29),
            'partner_id': cls.user_portal.partner_id.id,
        })

        cls.subscription_run_2020_03_31 = SubscriptionRun.create({
            'name': "End Date 31/03/2020",
            'date_end': datetime.date(2020, 3, 31),
            'partner_id': cls.user_portal.partner_id.id,
        })

        cls.subscription_run_2020_06_30 = SubscriptionRun.create({
            'name': "End Date 30/06/2020",
            'date_end': datetime.date(2020, 6, 30),
            'partner_id': cls.user_portal.partner_id.id,
        })

        cls.subscription_run_2020_12_31 = SubscriptionRun.create({
            'name': "End Date 31/12/2020",
            'date_end': datetime.date(2020, 12, 31),
            'partner_id': cls.user_portal.partner_id.id,
        })

    def _test_subscription_run(self, nbline, qty, subscription):

        subscription.action_calculer()

        self.assertTrue(len(subscription.line_ids) == nbline,
                        'Subscription Calculation error :  %s shoud have nb lines : %s, value found %s' % (
                            subscription.name, nbline, len(subscription.line_ids)))
        self.assertTrue(sum(subscription.line_ids.mapped('product_uom_qty')) == qty,
                        'Subscription Calculation error :  %s should have qty = %s, value found : %s' % (
                            subscription.name, qty, sum(subscription.line_ids.mapped('product_uom_qty'))))

    def _test_subscription_run_cancel(self, subscription, nbline, qty):
        self._test_subscription_run(nbline, qty, subscription)

        subscription.action_cancel()
        self.assertTrue(subscription.state == 'cancel',
                        'Subscription Cancellation error :  %s should be cancelled' % subscription.name)
        self.assertTrue(len(subscription.line_ids) == 0,
                        'Subscription Cancellation error :  %s should have no lines' % subscription.name)

    def _test_subscription_commit(self, subscriptionrun, nbline, qty, nborder):
        if subscriptionrun.state == 'cancel':
            subscriptionrun.write({'state': 'draft'})

        self._test_subscription_run(nbline, qty, subscriptionrun)

        subscriptionrun.action_valider()
        subscriptionrun.line_ids.mapped('phi_subscription_subscription_id')._compute_date_next()

        self.assertTrue(subscriptionrun.state == 'done',
                        'Subscription commit error :  %s should be done, value found %s' % (
                            subscriptionrun.name, subscriptionrun.state))
        self.assertTrue(len(subscriptionrun.sale_order_ids) == nborder,
                        'Subscription commit error :  %s should have %s, value found %s' % (
                            subscriptionrun.name, nborder, len(subscriptionrun.sale_order_ids)))

    def test_subscription_run_cancel(self):
        self._test_subscription_run_cancel(self.subscription_run_2019_12_31, 0, 0)
        self._test_subscription_run_cancel(self.subscription_run_2020_01_01, 1, 1)
        self._test_subscription_run_cancel(self.subscription_run_2020_01_06, 2, 7)
        self._test_subscription_run_cancel(self.subscription_run_2020_01_07, 2, 8)
        self._test_subscription_run_cancel(self.subscription_run_2020_01_14, 2, 16)
        self._test_subscription_run_cancel(self.subscription_run_2020_01_21, 2, 24)
        self._test_subscription_run_cancel(self.subscription_run_2020_01_31, 3, 36)
        self._test_subscription_run_cancel(self.subscription_run_2020_02_29, 4, 71)
        self._test_subscription_run_cancel(self.subscription_run_2020_03_31, 5, 109)
        self._test_subscription_run_cancel(self.subscription_run_2020_06_30, 6, 220)
        self._test_subscription_run_cancel(self.subscription_run_2020_12_31, 7, 443)

    def test_subscription_run_commit(self):

        self._test_subscription_commit(self.subscription_run_2020_01_01, 1, 1, 1)
        self._test_subscription_commit(self.subscription_run_2020_01_06, 2, 6, 1)
        self._test_subscription_commit(self.subscription_run_2020_01_07, 1, 1, 1)
        self._test_subscription_commit(self.subscription_run_2020_01_14, 2, 8, 1)
        self._test_subscription_commit(self.subscription_run_2020_01_21, 2, 8, 1)
        self._test_subscription_commit(self.subscription_run_2020_01_31, 3, 12, 1)
        self._test_subscription_commit(self.subscription_run_2020_02_29, 4, 35, 1)
        self._test_subscription_commit(self.subscription_run_2020_03_31, 4, 38, 1)
        self._test_subscription_commit(self.subscription_run_2020_06_30, 6, 111, 1)
        self._test_subscription_commit(self.subscription_run_2020_12_31, 7, 223, 1)

    def test_subscription_with_qty(self):

        user_env = self.env['res.users'].with_context({'no_reset_password': True})
        subscription_env = self.env['phi_subscription.subscription']
        subscription_run_env = self.env['phi_subscription.subscription_run']

        group_portal_id = self.env.ref('base.group_portal').id
        user_portal = user_env.create({
            'name': 'test qty',
            'login': 'test1',
            'email': 'test@example.com',
            'groups_id': [(6, 0, [group_portal_id])],
            'property_account_payable_id': self.account_payable.id,
            'property_account_receivable_id': self.account_receivable.id,
        })

        subscription_monthly = subscription_env.create({
            'name': 'SubscriptionmonthlyQty',
            'partner_id': user_portal.partner_id.id,
            'product_id': self.product_tmpl_monthly.product_variant_id.id,
            'date_start': datetime.date(2020, 1, 1),
            'product_qty': 12,
            'uom_id': self.product_tmpl_monthly.product_variant_id.uom_id,
        })

        subscription_run = subscription_run_env.create({
            'name' : "End Date 31/12/2019",
            'date_end': datetime.date(2020, 12, 31),
            'partner_id': user_portal.partner_id.id,
        })

        subscription_run.action_calculer()
        nbline = 1
        qty = 12
        date_end = datetime.date(2020, 12, 31)

        self.assertTrue(len(subscription_run.line_ids) == nbline,
                        'Subscription Calculation error :  %s shoud have nb lines : %s, value found %s' % (
                            subscription_run.name, nbline, len(subscription_run.line_ids)))
        self.assertTrue(sum(subscription_run.line_ids.mapped('product_uom_qty')) == qty,
                        'Subscription Calculation error :  %s should have qty = %s, value found : %s' % (
                            subscription_run.name, qty, sum(subscription_run.line_ids.mapped('product_uom_qty'))))
        self.assertTrue(subscription_run.line_ids[0].date_end_cal == date_end,
                        'Subscription Calculation error :  %s shoud have date end : %s, value found %s' % (
                            subscription_run.name, date_end, subscription_run.line_ids[0].date_end_cal))

    def test_subscription_with_prorata(self):

        user_env = self.env['res.users'].with_context({'no_reset_password': True})
        subscription_env = self.env['phi_subscription.subscription']
        subscription_run_env = self.env['phi_subscription.subscription_run']
        ProductTmpl = self.env['product.template']

        group_portal_id = self.env.ref('base.group_portal').id
        user_portal = user_env.create({
            'name': 'test prorata',
            'login': 'test1',
            'email': 'test@example.com',
            'groups_id': [(6, 0, [group_portal_id])],
            'property_account_payable_id': self.account_payable.id,
            'property_account_receivable_id': self.account_receivable.id,
        })

        product_tmpl_monthly = ProductTmpl.create({
            'name': 'TestProductMonthly',
            'type': 'service',
            'subscription_product': True,
            'period': 'monthly',
            'anticipation': 0,
            'uom_id': self.env.ref('uom.product_uom_unit').id,
            'price': 200.00,
            'taxes_id': [(6, 0, [self.tax_10.id])],
            'property_account_income_id': self.account_income.id,
        })

        subscription_monthly = subscription_env.create({
            'name': 'SubscriptionmonthlyQty',
            'partner_id': user_portal.partner_id.id,
            'product_id': product_tmpl_monthly.product_variant_id.id,
            'date_start': datetime.date(2020, 1, 15),
            'date_end': datetime.date(2020, 3, 15),
        })

        subscription_run = subscription_run_env.create({
            'name' : "End Date 31/01/2020",
            'date_end': datetime.date(2020, 1, 31),
            'partner_id': user_portal.partner_id.id,
        })

        subscription_run.action_calculer()
        subscription_run.action_valider()
        subscription_run.line_ids.mapped('phi_subscription_subscription_id')._compute_date_next()
        nbline = 1
        qty = 0.567

        date_start = datetime.date(2020, 1, 15)
        date_end = datetime.date(2020, 1, 31)

        self.assertTrue(len(subscription_run.line_ids) == nbline,
                        'Subscription Calculation prorata error :  %s shoud have nb lines : %s, value found %s' % (
                            subscription_run.name, nbline, len(subscription_run.line_ids)))
        self.assertTrue(round(sum(subscription_run.line_ids.mapped('product_uom_qty')), 3) == qty,
                        'Subscription Calculation prorata error :  %s should have qty = %s, value found : %s' % (
                            subscription_run.name, qty, round(sum(subscription_run.line_ids.mapped('product_uom_qty')), 3)))
        self.assertTrue(subscription_run.line_ids[0].date_end_cal == date_end,
                        'Subscription Calculation prorata error :  %s shoud have date end : %s, value found %s' % (
                            subscription_run.name, date_end, subscription_run.line_ids[0].date_end_cal))
        self.assertTrue(subscription_run.line_ids[0].date_start_cal == date_start,
                        'Subscription Calculation prorata error :  %s shoud have date end : %s, value found %s' % (
                            subscription_run.name, date_start, subscription_run.line_ids[0].date_start_cal))

        subscription_run2 = subscription_run_env.create({
            'name': "End Date 29/02/2020",
            'date_end': datetime.date(2020, 2, 29),
            'partner_id': user_portal.partner_id.id,
        })

        subscription_run2.action_calculer()
        subscription_run2.action_valider()
        subscription_run2.line_ids.mapped('phi_subscription_subscription_id')._compute_date_next()

        nbline = 1
        qty = 1

        date_start = datetime.date(2020, 2, 1)
        date_end = datetime.date(2020, 2, 29)

        self.assertTrue(len(subscription_run2.line_ids) == nbline,
                        'Subscription Calculation prorata error :  %s shoud have nb lines : %s, value found %s' % (
                            subscription_run2.name, nbline, len(subscription_run2.line_ids)))
        self.assertTrue(sum(subscription_run2.line_ids.mapped('product_uom_qty')) == qty,
                        'Subscription Calculation prorata error :  %s should have qty = %s, value found : %s' % (
                            subscription_run2.name, qty, sum(subscription_run2.line_ids.mapped('product_uom_qty'))))
        self.assertTrue(subscription_run2.line_ids[0].date_end_cal == date_end,
                        'Subscription Calculation prorata error :  %s shoud have date end : %s, value found %s' % (
                            subscription_run2.name, date_end, subscription_run2.line_ids[0].date_end_cal))
        self.assertTrue(subscription_run2.line_ids[0].date_start_cal == date_start,
                        'Subscription Calculation prorata error :  %s shoud have date end : %s, value found %s' % (
                            subscription_run2.name, date_start, subscription_run2.line_ids[0].date_start_cal))

        subscription_run3 = subscription_run_env.create({
            'name': "End Date 31/03/2020",
            'date_end': datetime.date(2020, 3, 31),
            'partner_id': user_portal.partner_id.id,
        })

        subscription_run3.action_calculer()
        subscription_run3.action_valider()
        subscription_run3.line_ids.mapped('phi_subscription_subscription_id')._compute_date_next()

        nbline = 1
        qty = 0.5

        date_start = datetime.date(2020, 3, 1)
        date_end = datetime.date(2020, 3, 15)

        self.assertTrue(len(subscription_run3.line_ids) == nbline,
                        'Subscription Calculation prorata error :  %s shoud have nb lines : %s, value found %s' % (
                            subscription_run3.name, nbline, len(subscription_run3.line_ids)))
        self.assertTrue(sum(subscription_run3.line_ids.mapped('product_uom_qty')) == qty,
                        'Subscription Calculation prorata error :  %s should have qty = %s, value found : %s' % (
                            subscription_run3.name, qty, sum(subscription_run3.line_ids.mapped('product_uom_qty'))))
        self.assertTrue(subscription_run3.line_ids[0].date_end_cal == date_end,
                        'Subscription Calculation prorata error :  %s shoud have date end : %s, value found %s' % (
                            subscription_run3.name, date_end, subscription_run3.line_ids[0].date_end_cal))
        self.assertTrue(subscription_run3.line_ids[0].date_start_cal == date_start,
                        'Subscription Calculation prorata error :  %s shoud have date end : %s, value found %s' % (
                            subscription_run3.name, date_start, subscription_run3.line_ids[0].date_start_cal))

    def test_subscription_with_prorata_full(self):

        user_env = self.env['res.users'].with_context({'no_reset_password': True})
        subscription_env = self.env['phi_subscription.subscription']
        subscription_run_env = self.env['phi_subscription.subscription_run']
        ProductTmpl = self.env['product.template']

        group_portal_id = self.env.ref('base.group_portal').id
        user_portal = user_env.create({
            'name': 'test prorata',
            'login': 'test1',
            'email': 'test@example.com',
            'groups_id': [(6, 0, [group_portal_id])],
            'property_account_payable_id': self.account_payable.id,
            'property_account_receivable_id': self.account_receivable.id,
        })

        product_tmpl_monthly = ProductTmpl.create({
            'name': 'TestProductMonthly',
            'type': 'service',
            'subscription_product': True,
            'period': 'monthly',
            'anticipation': 0,
            'proportion': 'full',
            'uom_id': self.env.ref('uom.product_uom_unit').id,
            'price': 200.00,
            'taxes_id': [(6, 0, [self.tax_10.id])],
            'property_account_income_id': self.account_income.id,
        })

        subscription_monthly = subscription_env.create({
            'name': 'SubscriptionmonthlyQty',
            'partner_id': user_portal.partner_id.id,
            'product_id': product_tmpl_monthly.product_variant_id.id,
            'date_start': datetime.date(2020, 1, 15),
            'date_end': datetime.date(2020, 3, 15),
        })

        subscription_run = subscription_run_env.create({
            'name' : "End Date 31/01/2020",
            'date_end': datetime.date(2020, 1, 31),
            'partner_id': user_portal.partner_id.id,
        })

        subscription_run.action_calculer()
        subscription_run.action_valider()
        subscription_run.line_ids.mapped('phi_subscription_subscription_id')._compute_date_next()
        nbline = 1
        qty = 1

        date_start = datetime.date(2020, 1, 15)
        date_end = datetime.date(2020, 1, 31)

        self.assertTrue(len(subscription_run.line_ids) == nbline,
                        'Subscription Calculation prorata error :  %s shoud have nb lines : %s, value found %s' % (
                            subscription_run.name, nbline, len(subscription_run.line_ids)))
        self.assertTrue(round(sum(subscription_run.line_ids.mapped('product_uom_qty')), 3) == qty,
                        'Subscription Calculation prorata error :  %s should have qty = %s, value found : %s' % (
                            subscription_run.name, qty, round(sum(subscription_run.line_ids.mapped('product_uom_qty')), 3)))
        self.assertTrue(subscription_run.line_ids[0].date_end_cal == date_end,
                        'Subscription Calculation prorata error :  %s shoud have date end : %s, value found %s' % (
                            subscription_run.name, date_end, subscription_run.line_ids[0].date_end_cal))
        self.assertTrue(subscription_run.line_ids[0].date_start_cal == date_start,
                        'Subscription Calculation prorata error :  %s shoud have date end : %s, value found %s' % (
                            subscription_run.name, date_start, subscription_run.line_ids[0].date_start_cal))

        subscription_run2 = subscription_run_env.create({
            'name': "End Date 29/02/2020",
            'date_end': datetime.date(2020, 2, 29),
            'partner_id': user_portal.partner_id.id,
        })

        subscription_run2.action_calculer()
        subscription_run2.action_valider()
        subscription_run2.line_ids.mapped('phi_subscription_subscription_id')._compute_date_next()

        nbline = 1
        qty = 1

        date_start = datetime.date(2020, 2, 1)
        date_end = datetime.date(2020, 2, 29)

        self.assertTrue(len(subscription_run2.line_ids) == nbline,
                        'Subscription Calculation prorata error :  %s shoud have nb lines : %s, value found %s' % (
                            subscription_run2.name, nbline, len(subscription_run2.line_ids)))
        self.assertTrue(sum(subscription_run2.line_ids.mapped('product_uom_qty')) == qty,
                        'Subscription Calculation prorata error :  %s should have qty = %s, value found : %s' % (
                            subscription_run2.name, qty, sum(subscription_run2.line_ids.mapped('product_uom_qty'))))
        self.assertTrue(subscription_run2.line_ids[0].date_end_cal == date_end,
                        'Subscription Calculation prorata error :  %s shoud have date end : %s, value found %s' % (
                            subscription_run2.name, date_end, subscription_run2.line_ids[0].date_end_cal))
        self.assertTrue(subscription_run2.line_ids[0].date_start_cal == date_start,
                        'Subscription Calculation prorata error :  %s shoud have date end : %s, value found %s' % (
                            subscription_run2.name, date_start, subscription_run2.line_ids[0].date_start_cal))

        subscription_run3 = subscription_run_env.create({
            'name': "End Date 31/03/2020",
            'date_end': datetime.date(2020, 3, 31),
            'partner_id': user_portal.partner_id.id,
        })

        subscription_run3.action_calculer()
        subscription_run3.action_valider()
        subscription_run3.line_ids.mapped('phi_subscription_subscription_id')._compute_date_next()

        nbline = 1
        qty = 1

        date_start = datetime.date(2020, 3, 1)
        date_end = datetime.date(2020, 3, 15)

        self.assertTrue(len(subscription_run3.line_ids) == nbline,
                        'Subscription Calculation prorata error :  %s shoud have nb lines : %s, value found %s' % (
                            subscription_run3.name, nbline, len(subscription_run3.line_ids)))
        self.assertTrue(sum(subscription_run3.line_ids.mapped('product_uom_qty')) == qty,
                        'Subscription Calculation prorata error :  %s should have qty = %s, value found : %s' % (
                            subscription_run3.name, qty, sum(subscription_run3.line_ids.mapped('product_uom_qty'))))
        self.assertTrue(subscription_run3.line_ids[0].date_end_cal == date_end,
                        'Subscription Calculation prorata error :  %s shoud have date end : %s, value found %s' % (
                            subscription_run3.name, date_end, subscription_run3.line_ids[0].date_end_cal))
        self.assertTrue(subscription_run3.line_ids[0].date_start_cal == date_start,
                        'Subscription Calculation prorata error :  %s shoud have date end : %s, value found %s' % (
                            subscription_run3.name, date_start, subscription_run3.line_ids[0].date_start_cal))

    def test_subscription_with_prorata_none(self):

        user_env = self.env['res.users'].with_context({'no_reset_password': True})
        subscription_env = self.env['phi_subscription.subscription']
        subscription_run_env = self.env['phi_subscription.subscription_run']
        ProductTmpl = self.env['product.template']

        group_portal_id = self.env.ref('base.group_portal').id
        user_portal = user_env.create({
            'name': 'test prorata',
            'login': 'test1',
            'email': 'test@example.com',
            'groups_id': [(6, 0, [group_portal_id])],
            'property_account_payable_id': self.account_payable.id,
            'property_account_receivable_id': self.account_receivable.id,
        })

        product_tmpl_monthly = ProductTmpl.create({
            'name': 'TestProductMonthly',
            'type': 'service',
            'subscription_product': True,
            'period': 'monthly',
            'anticipation': 0,
            'proportion': 'none',
            'uom_id': self.env.ref('uom.product_uom_unit').id,
            'price': 200.00,
            'taxes_id': [(6, 0, [self.tax_10.id])],
            'property_account_income_id': self.account_income.id,
        })

        subscription_monthly = subscription_env.create({
            'name': 'SubscriptionmonthlyQty',
            'partner_id': user_portal.partner_id.id,
            'product_id': product_tmpl_monthly.product_variant_id.id,
            'date_start': datetime.date(2020, 1, 15),
            'date_end': datetime.date(2020, 3, 15),
        })

        subscription_run = subscription_run_env.create({
            'name' : "End Date 31/01/2020",
            'date_end': datetime.date(2020, 1, 31),
            'partner_id': user_portal.partner_id.id,
        })

        subscription_run.action_calculer()
        subscription_run.action_valider()
        subscription_run.line_ids.mapped('phi_subscription_subscription_id')._compute_date_next()
        nbline = 0

        self.assertTrue(len(subscription_run.line_ids) == nbline,
                        'Subscription Calculation prorata error :  %s shoud have nb lines : %s, value found %s' % (
                            subscription_run.name, nbline, len(subscription_run.line_ids)))

        subscription_run2 = subscription_run_env.create({
            'name': "End Date 29/02/2020",
            'date_end': datetime.date(2020, 2, 29),
            'partner_id': user_portal.partner_id.id,
        })

        subscription_run2.action_calculer()
        subscription_run2.action_valider()
        subscription_run2.line_ids.mapped('phi_subscription_subscription_id')._compute_date_next()

        nbline = 1
        qty = 1

        date_start = datetime.date(2020, 1, 15)
        date_end = datetime.date(2020, 2, 29)

        self.assertTrue(len(subscription_run2.line_ids) == nbline,
                        'Subscription Calculation prorata error :  %s shoud have nb lines : %s, value found %s' % (
                            subscription_run2.name, nbline, len(subscription_run2.line_ids)))
        self.assertTrue(sum(subscription_run2.line_ids.mapped('product_uom_qty')) == qty,
                        'Subscription Calculation prorata error :  %s should have qty = %s, value found : %s' % (
                            subscription_run2.name, qty, sum(subscription_run2.line_ids.mapped('product_uom_qty'))))
        self.assertTrue(subscription_run2.line_ids[0].date_end_cal == date_end,
                        'Subscription Calculation prorata error :  %s shoud have date end : %s, value found %s' % (
                            subscription_run2.name, date_end, subscription_run2.line_ids[0].date_end_cal))
        self.assertTrue(subscription_run2.line_ids[0].date_start_cal == date_start,
                        'Subscription Calculation prorata error :  %s shoud have date end : %s, value found %s' % (
                            subscription_run2.name, date_start, subscription_run2.line_ids[0].date_start_cal))

        subscription_run3 = subscription_run_env.create({
            'name': "End Date 31/03/2020",
            'date_end': datetime.date(2020, 3, 31),
            'partner_id': user_portal.partner_id.id,
        })

        subscription_run3.action_calculer()
        subscription_run3.action_valider()
        subscription_run3.line_ids.mapped('phi_subscription_subscription_id')._compute_date_next()

        nbline = 0


        self.assertTrue(len(subscription_run3.line_ids) == nbline,
                        'Subscription Calculation prorata error :  %s shoud have nb lines : %s, value found %s' % (
                            subscription_run3.name, nbline, len(subscription_run3.line_ids)))

    def test_subscription_with_anticipation_1(self):

        user_env = self.env['res.users'].with_context({'no_reset_password': True})
        subscription_env = self.env['phi_subscription.subscription']
        subscription_run_env = self.env['phi_subscription.subscription_run']
        ProductTmpl = self.env['product.template']

        group_portal_id = self.env.ref('base.group_portal').id
        user_portal = user_env.create({
            'name': 'test prorata',
            'login': 'test1',
            'email': 'test@example.com',
            'groups_id': [(6, 0, [group_portal_id])],
            'property_account_payable_id': self.account_payable.id,
            'property_account_receivable_id': self.account_receivable.id,
        })

        product_tmpl_monthly = ProductTmpl.create({
            'name': 'TestProductMonthlyAnticipation1',
            'type': 'service',
            'subscription_product': True,
            'period': 'monthly',
            'anticipation': 1,
            'proportion': 'none',
            'uom_id': self.env.ref('uom.product_uom_unit').id,
            'price': 200.00,
            'taxes_id': [(6, 0, [self.tax_10.id])],
            'property_account_income_id': self.account_income.id,
        })

        subscription_monthly = subscription_env.create({
            'name': 'SubscriptionmonthlyQty',
            'partner_id': user_portal.partner_id.id,
            'product_id': product_tmpl_monthly.product_variant_id.id,
            'date_start': datetime.date(2020, 1, 1),
        })

        subscription_run2 = subscription_run_env.create({
            'name' : "End Date 31/01/2020",
            'date_end': datetime.date(2020, 1, 1),
            'partner_id': user_portal.partner_id.id,
        })

        subscription_run2.action_calculer()
        nbline = 1
        qty = 1

        date_start = datetime.date(2020, 1, 1)
        date_end = datetime.date(2020, 1, 31)

        self.assertTrue(len(subscription_run2.line_ids) == nbline,
                        'Subscription Calculation prorata error :  %s shoud have nb lines : %s, value found %s' % (
                            subscription_run2.name, nbline, len(subscription_run2.line_ids)))
        self.assertTrue(sum(subscription_run2.line_ids.mapped('product_uom_qty')) == qty,
                        'Subscription Calculation prorata error :  %s should have qty = %s, value found : %s' % (
                            subscription_run2.name, qty, sum(subscription_run2.line_ids.mapped('product_uom_qty'))))
        self.assertTrue(subscription_run2.line_ids[0].date_end_cal == date_end,
                        'Subscription Calculation prorata error :  %s shoud have date end : %s, value found %s' % (
                            subscription_run2.name, date_end, subscription_run2.line_ids[0].date_end_cal))
        self.assertTrue(subscription_run2.line_ids[0].date_start_cal == date_start,
                        'Subscription Calculation prorata error :  %s shoud have date end : %s, value found %s' % (
                            subscription_run2.name, date_start, subscription_run2.line_ids[0].date_start_cal))

    def test_subscription_with_anticipation_2(self):

        user_env = self.env['res.users'].with_context({'no_reset_password': True})
        subscription_env = self.env['phi_subscription.subscription']
        subscription_run_env = self.env['phi_subscription.subscription_run']
        ProductTmpl = self.env['product.template']

        group_portal_id = self.env.ref('base.group_portal').id
        user_portal = user_env.create({
            'name': 'test prorata',
            'login': 'test1',
            'email': 'test@example.com',
            'groups_id': [(6, 0, [group_portal_id])],
            'property_account_payable_id': self.account_payable.id,
            'property_account_receivable_id': self.account_receivable.id,
        })

        product_tmpl_monthly = ProductTmpl.create({
            'name': 'TestProductMonthlyAnticipation1',
            'type': 'service',
            'subscription_product': True,
            'period': 'monthly',
            'anticipation': -1,
            'proportion': 'none',
            'uom_id': self.env.ref('uom.product_uom_unit').id,
            'price': 200.00,
            'taxes_id': [(6, 0, [self.tax_10.id])],
            'property_account_income_id': self.account_income.id,
        })

        subscription_monthly = subscription_env.create({
            'name': 'SubscriptionmonthlyQty',
            'partner_id': user_portal.partner_id.id,
            'product_id': product_tmpl_monthly.product_variant_id.id,
            'date_start': datetime.date(2020, 1, 1),
        })

        subscription_run2 = subscription_run_env.create({
            'name' : "End Date 29/02/2020",
            'date_end': datetime.date(2020, 2, 29),
            'partner_id': user_portal.partner_id.id,
        })

        subscription_run2.action_calculer()

        nbline = 1
        qty = 1

        date_start = datetime.date(2020, 1, 1)
        date_end = datetime.date(2020, 1, 31)

        self.assertTrue(len(subscription_run2.line_ids) == nbline,
                        'Subscription Calculation prorata error :  %s shoud have nb lines : %s, value found %s' % (
                            subscription_run2.name, nbline, len(subscription_run2.line_ids)))
        self.assertTrue(sum(subscription_run2.line_ids.mapped('product_uom_qty')) == qty,
                        'Subscription Calculation prorata error :  %s should have qty = %s, value found : %s' % (
                            subscription_run2.name, qty, sum(subscription_run2.line_ids.mapped('product_uom_qty'))))
        self.assertTrue(subscription_run2.line_ids[0].date_end_cal == date_end,
                        'Subscription Calculation prorata error :  %s shoud have date end : %s, value found %s' % (
                            subscription_run2.name, date_end, subscription_run2.line_ids[0].date_end_cal))
        self.assertTrue(subscription_run2.line_ids[0].date_start_cal == date_start,
                        'Subscription Calculation prorata error :  %s shoud have date end : %s, value found %s' % (
                            subscription_run2.name, date_start, subscription_run2.line_ids[0].date_start_cal))
