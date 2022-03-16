# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'Abeille : Millesime',
    'version': '14.0.0.0',
    'summary': 'Millesime',
    'description': """
Ajout de la table millésime.
Plusieurs millésimes peuvent être actifs à la fois.

Feature :
- Table millésime
- Menu millésime (Ventes -> Configuration -> Millesime)
- Vue liste millésime avec 3 filtres (Actifs/Inactifs/Actifs et Inactifs)
- Selection du millésime dans le devis
- Affichage du millésime dans la facture (readonly)
- Group By millésime dans la vue liste des tâches
- Champ millésime dans les tâches
""",
    'author': 'Abeille',
    'website': 'https://aca-consult.com/',
    'depends': [
        'sale_management',
        'project',
    ],
    'data': [
        'views/millesime.xml',
        'views/project_task_views.xml',
        'views/sale_views.xml',
        'views/account_move.xml',
        'security/ir.model.access.csv',
    ],
    'application': True,
    'license': 'OEEL-1',
}
