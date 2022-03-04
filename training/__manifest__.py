# -*- coding: utf-8 -*-
{
    'name': "Module d'entrainement",

    'summary': """
        Résumé
        """,

    'description': """
        Description
    """,

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '15.0.0.0',
    'license': 'LGPL-3',
    # any module necessary for this one to work correctly
    'depends': ["sale"],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        # 'views/module_entrainement.xml',
        # 'views/module2_entrainement.xml',
        'views/sale.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ]
}
