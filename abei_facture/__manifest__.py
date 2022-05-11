# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'Abeille : Facture',
    'version': '14.0.0.0',
    'summary': 'Facture',
    'description': """

Features :
Dans la vue liste des factures :
- •	Ajout d'une colonne "Piece envoyée"

""",
    'author': 'Abeille',
    'website': 'https://aca-consult.com/',
    'depends': [
        'account',
    ],
    'data': [
        'views/account_move_views.xml',
    ],
    'application': True,
    'license': 'OEEL-1',
}
