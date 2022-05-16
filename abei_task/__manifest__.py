# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'Abeille : Tâche',
    'version': '14.0.0.0',
    'summary': 'Tâche',
    'description': """

Features :
    - Ajoute un bandeau coloré sur la gauche des tâches dans la vue Kanban. Le bandeau prend pour couleur la couleur définie dans "l'étiquette projet" de la tâche.

""",
    'author': 'Abeille',
    'website': 'https://aca-consult.com/',
    'depends': [
        'project',
    ],
    'data': [
        'views/project_views.xml',
    ],
    'application': True,
    'license': 'OEEL-1',
}
