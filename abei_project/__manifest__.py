# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'Abeille : Project',
    'version': '14.0.0.0',
    'summary': 'Project',
    'description': """
Ajout de divers filtre dans vues project.project et project.task :
- Administratif
- CAC
- Comptable
- Juridique
- Social
- Informatique

- Ajout champ "Etiquettes de projet" dans la vue formulaire project.project
""",
    'author': 'Abeille',
    'website': 'https://aca-consult.com/',
    'depends': [
        'project',
    ],
    'data': [
        'views/project_project.xml',
        'views/project_task.xml',
    ],
    'application': True,
    'license': 'OEEL-1',
}