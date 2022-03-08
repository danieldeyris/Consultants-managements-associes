# -*- coding: utf-8 -*-
{
    'name': "Phidias : Abonnements",

    'summary': """
        Terme à échoir / terme échu
        """,

    'description': """
        Terme à échoir / terme échu
    """,

    'author': "Phidias",
    'website': "http://www.phidias.fr",


    'category': 'Uncategorized',
    'version': '14.0.0.0',

    # any module necessary for this one to work correctly
    'depends': [
        'sale_subscription',
        'account',
    ],

    # always loaded
    'data': [
        'views/sale_subscription.xml',
    ],
}
