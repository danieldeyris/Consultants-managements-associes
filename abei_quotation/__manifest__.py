# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'Abeille : Quotation',
    'version': '14.0.0.0',
    'summary': 'Quotation',
    'description': """
Ce module ajoute dans les "order lines" du devis la possibilité de sélectionner le collaborateur affecté (Employee)
price_unit => prend alors pour valeur le taux de facturation horaire du collaborateur.

""",
    'author': 'Abeille',
    'website': 'https://aca-consult.com/',
    'depends': [
        'hr',
        'sale_management',
        'abei_employee_information',
    ],
    'data': [
        'views/sale_views.xml',
    ],
    'application': True,
    'license': 'OEEL-1',
}