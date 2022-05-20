# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'Abeille : Article',
    'version': '14.0.0.0',
    'summary': 'Article',
    'description': """

Features :
Ajout étiquette sur la vue formulaire articles (Comptabilité, Juridique, ...)
Ajout de l'étiquette sur les vues : Kanban, Liste
Ajout de filtres sur l'étiquette dans les vues : Kanban, Liste

""",
    'author': 'Abeille',
    'website': 'https://aca-consult.com/',
    'depends': [
        'account',
        'project',
    ],
    'data': [
        'views/product_template_views.xml',
    ],
    'application': True,
    'license': 'OEEL-1',
}
