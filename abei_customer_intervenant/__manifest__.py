# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'Abeille : Customer Intervenants',
    'version': '14.0.0.0',
    'summary': 'Customer Intervenants',
    'description': """
Ce module permet de gérer les collaborateurs intervenant dans des dossiers clients

Feature :
- Onglet Intervenants
- Ajout champ refClient pour l'import/export de données
""",
    'author': 'Abeille',
    'website': 'https://aca-consult.com/',
    'depends': [
        'contacts',
        'hr',
    ],
    'data': [
        'views/res_partner.xml',
    ],
    'application': True,
    'license': 'OEEL-1',
}
