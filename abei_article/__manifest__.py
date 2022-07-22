# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'Abeille : Article',
    'version': '14.0.0.0',
    'summary': 'Article',
    'description': """

Features :
- Ajout étiquette sur la vue formulaire articles (Comptabilité, Juridique, ...)
- Ajout de l'étiquette sur les vues : Kanban, Liste
- Ajout de filtres sur l'étiquette dans les vues : Kanban, Liste
- Dans le devis, lors de la sélection d'un article, si une 'description vente' est definie pour l'article
 alors lors de la selection de cet article dans le devis, la description (article du devis) = description vente (article), sinon description (article du devis) = libelle (article)
- Ajout d'une numérotation pour classifier les articles
- Ajout case à cocher pour les articles étant des bulletins de salaire.
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
