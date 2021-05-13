# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'Customer info',
    'version': '14.0.0.0',
    'category': 'Sales',
    'summary': 'Generate recurring invoices/orders and manage renewals',
    'description': """
This module allows you to manage subscriptions.

Features:
    - Create & edit subscriptions
    - Modify subscriptions with sales orders
    - Generate invoice automatically at fixed intervals
""",
    'author': 'Phidias',
    'website': 'https://www.phidias.fr',
    'depends': [
        'sale_management',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/fiscal_type.xml',
        'views/res_partner.xml',
        'views/social_regime.xml',
        'views/vat_type.xml',
        'views/legal_type.xml',
        'views/social_type.xml',
        'views/activity_type.xml',
    ],
    'application': True,
    'license': 'OEEL-1',
}
