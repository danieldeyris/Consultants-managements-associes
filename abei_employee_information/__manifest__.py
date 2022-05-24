# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'Abeille : Employee Information',
    'version': '14.0.0.0',
    'summary': 'Employee Information',
    'description': """
Ce module ajoute des informations sur le matériel remis à l'employé.
Ajout champ de renseignement EC Inscrit (oui/non)
Ajout champ Taux Facturation

Feature :
- Checkbox EC Inscrit
- HR Settings -> Taux Facturation
- Onglet Matériel (Imei, Pin, Puk)
""",
    'author': 'Abeille',
    'website': 'https://aca-consult.com/',
    'depends': [
        'hr',
        'timesheet_grid',
    ],
    'data': [
        'views/hr_employee_views.xml',
    ],
    'application': True,
    'license': 'OEEL-1',
}
