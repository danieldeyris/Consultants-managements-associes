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

Dans le projet, vérification transfert de tâche d'une étape à une autre étape.
Si étape flaggée comme necessitant une saisie de temps ou de bulletins (module abei_project_stage_timesheet) vérification validité, sinon, refus de transfert
""",
    'author': 'Abeille',
    'website': 'https://aca-consult.com/',
    'depends': [
        'project',
        'abei_project_stage_timesheet',
        'abei_feuille_temps',
    ],
    'data': [
        'views/project_project.xml',
        'views/project_task.xml',
    ],
    'application': True,
    'license': 'OEEL-1',
}