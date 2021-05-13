# -*- coding: utf-8 -*-
{
    'name': "Compte analytique sur le tiers",

    'summary': """
        Compte analytique sur le tiers
        """,

    'description': """
        Compte analytique sur le tiers
    """,

    'author': "Phidias",
    'website': "http://www.phidias.fr",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '14.0.0.0',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'account',
        'sale_management',
        'purchase',
        'account_batch_payment',
    ],

    # always loaded
    'data': [
        'views/res_partner.xml',
        'views/purchase_order.xml',
        'views/sale_order.xml',
        'views/account_move.xml',
        'views/account_payment.xml',
        'views/account_batch_payment.xml',
        'views/res_users_views.xml',
    ],
}
