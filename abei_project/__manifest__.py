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
- ajout automatique d'une ligne de temps en fonction du temps prédéfinie + notification pour prévenir l'utilisateur d'un ajout de ligne de temps.

si non : 
- message prévenant de la nécessité de saisir le temps.

Mise en place d'une vérification lors de la modification d'un tâche.
Si un employé n'ayant pas le même département métier (etiquettes projet) que la tâche essai de la modifier, ou que la tâche ne lui est pas directement affectée, avertissement.

Dans la vue liste des tâches, mise en place de :
- Un champ "ajouter temps" pour réaliser une saisie rapide, sans avoir à entrer dans la tâche.
- Un champ "ajouter quantité" pour réaliser une saisie de quantité, sans avoir à entrer dans la tâche.
- Un option d'action "Clôturer tâche(s) et saisie forfaitaire des temps (si possible)", pour cloturer la tâche et saisie auto des temps, sans avoir à entrer dans la tâche.
""",
    'author': 'Abeille',
    'website': 'https://aca-consult.com/',
    'depends': [
        'project',
        'abei_feuille_temps',
        'abei_article',
        'abei_quotation',
        'web_notify',
    ],
    'data': [
        'views/res_user_views.xml',
        'views/hr_employee_views.xml',
        'views/project_project.xml',
        'views/project_task.xml',
    ],
    'application': True,
    'license': 'OEEL-1',
}