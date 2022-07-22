# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'Abeille : Signature',
    'version': '14.0.0.0',
    'summary': 'Signature',
    'description': """
    Ajout d'un onglet "Signature email" dans la vue user pour permettre l'ajout de plusieures signatures multi compagnie
""",
    'author': 'Abeille',
    'website': 'https://aca-consult.com/',
    'depends': [
        'base',
        'mail',
    ],
    'data': [
        'views/mail_data.xml',
        'views/res_user_views.xml',
        'security/ir.model.access.csv',
    ],
    'application': True,
    'license': 'OEEL-1',
}
