# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'Abeille : Project Stage Timesheet',
    'version': '14.0.0.0',
    'category': 'Sales',
    'summary': 'Project Stage Timesheet',
    'description': """
    Ce module permet de forcer la saisie des temps/saisie des quantité lors d'une étape (Projet --> Etape)
    
    Features :
    - Ajout d'un champ (boolean) "Saisie des temps obligatoire"
    - Ajout d'un champ (boolean) "Saisie de quantités obligatoire"

""",
    'author': 'Abeille',
    'website': 'https://aca-consult.com/',
    'depends': [
        'project',
        'hr_timesheet',
    ],
    'data': [
        'views/project_task_type.xml',
    ],
    'application': True,
    'license': 'OEEL-1',
}
