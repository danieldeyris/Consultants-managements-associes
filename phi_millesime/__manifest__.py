# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'Phidias : Millesime',
    'version': '14.0.0.0',
    'category': 'Sales',
    'summary': 'Customer Millesime',
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
        'project',
    ],
    'data': [
        'views/millesime.xml',
        'views/project_task_views.xml',
        'security/ir.model.access.csv',
    ],
    'application': True,
    'license': 'OEEL-1',
}
