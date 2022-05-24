# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'Abeille : Customer Renseignement',
    'version': '14.0.0.0',
    'summary': 'Customer Renseignement',
    'description': """
Ce module permet de gérer informations privées du client.

Feature :
- Onglet Renseignement
""",
    'author': 'Abeille',
    'website': 'https://aca-consult.com/',
    'depends': [
        'contacts',
        'customer_infos',
    ],
    'data': [
        'views/res_partner.xml',
    ],
    'application': True,
    'license': 'OEEL-1',
}
