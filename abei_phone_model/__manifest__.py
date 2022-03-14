# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'Abeille : Phone Model',
    'version': '14.0.0.0',
    'summary': 'Phone Model',
    'description': """
Ce module ajoute la notion de modèle de téléphone.
(Vue matériel - Employee)

Feature :
- Champ Modèle téléphone
""",
    'author': 'Abeille',
    'website': 'https://aca-consult.com/',
    'depends': [
        'hr',
        'abei_employee_information',
    ],
    'data': [
        'views/hr_employee_views.xml',
        'security/ir.model.access.csv',
    ],
    'application': True,
    'license': 'OEEL-1',
}
