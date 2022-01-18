# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'Phidias : Project Stage Timesheet',
    'version': '14.0.0.0',
    'category': 'Sales',
    'summary': 'Project Stage Timesheet',
    'description': """
This module allows you to force Timesheet on stage.

Features:
    - Create & edit subscriptions
    - Modify subscriptions with sales orders
    - Generate invoice automatically at fixed intervals
""",
    'author': 'Phidias',
    'website': 'https://www.phidias.fr',
    'depends': [
        'project',
        'hr_timesheet',
    ],
    'data': [
        'views/project_task_type.xml',
    ],
    'application': True,
    'license': 'OEEL-1',
}
