# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'Abeille : Customer Social Network',
    'version': '14.0.0.0',
    'summary': 'Customer Social Network',
    'description': """
Ce module permet de gérer les réseaux sociaux depuis la fiche client.

Feature :
- Onglet Réseaux Sociaux
""",
    'author': 'Abeille',
    'website': 'https://aca-consult.com/',
    'depends': [
        'contacts',
    ],
    'data': [
        'views/res_partner.xml',
    ],
    'application': True,
    'license': 'OEEL-1',
}
