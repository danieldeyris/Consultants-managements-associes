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

- Ajout champ "Type temps" dans la tâche. Par défaut récupère le type temps de l'article, mais peut être redéfini ici.

Dans le projet, vérification lors du transfert de tâche d'une étape à une autre étape.
Si l'étape est flaggée comme etant une etape de cloture :
- vérification si la tâche à saisie de temps obligatoires
si oui :
- Vérification si un type_temps est défini
si oui :
- ajout automatique d'une ligne de temps en fonction du temps prédéfinie

si non : 
- message prévenant de la nécessité de saisir le temps.

Idem pour la saisie des bulletins
""",
    'author': 'Abeille',
    'website': 'https://aca-consult.com/',
    'depends': [
        'project',
        'abei_feuille_temps',
        'abei_article',
    ],
    'data': [
        'views/project_project.xml',
        'views/project_task.xml',
    ],
    'application': True,
    'license': 'OEEL-1',
}