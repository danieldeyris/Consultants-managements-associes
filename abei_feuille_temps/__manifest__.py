# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'Abeille : Feuille de temps',
    'version': '14.0.0.0',
    'summary': 'Feuille de temps',
    'description': """

Features :
Dans la vue liste des feuilles de temps :
- • Ajout du champ 'Client'"
Dans la vue formulaire de la tâche :
- • Intervertion des onglets "Description" et "Feuilles de temps"


""",
    'author': 'Abeille',
    'website': 'https://aca-consult.com/',
    'depends': [
        'analytic',
        'contacts',
        'hr_timesheet',
        'timesheet_grid',
    ],
    'data': [
        'views/hr_timesheet_view.xml',
    ],
    'application': True,
    'license': 'OEEL-1',
}
