# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'Abeille : Acompte',
    'version': '14.0.0.0',
    'summary': 'Acompte',
    'description': """

Permet de facturer des acomptes de manière récurrente sur un devis contenant 1 ou plusieurs prestations facturées au temps passé. 
Le mode de facturation sur base acompte est incompatible avec la facturation par abonnement. On peut donc définir que :
• Le mode abonnement consiste à facturer de manière récurrente des montants sans que les temps passés donnent lieu à régularisation pour les prestations comprises dans l’abonnement (les articles au sens Odoo ayant un modèle d’abonnement défini)
• Le mode acompte consiste à facturer de manière régulière des montants qui seront régularisés lors de l’émission de factures de régularisation des temps passés. Seuls les articles non soumis à abonnement sont concernés par les acomptes.

Features :
Dans le devis, 3 nouveaux champs :
- •	Une case à cocher permet d’indiquer que la commande est soumise à acompte.
- •	Une liste déroulante "type d’acompte" qui permet d’indiquer la fréquence d’émission des factures d’acompte
- •	Un champs date de début d’acompte qui permet d’indiquer la période couverte.

Lorsque la commande est confirmée l’acompte est généré dans la gestion des acomptes.


""",
    'author': 'Abeille',
    'website': 'https://aca-consult.com/',
    'depends': [
        'sale_management',
        'abei_millesime',
    ],
    'data': [
        'views/sale_views.xml',
        'views/acompte.xml',
        'security/ir.model.access.csv',
    ],
    'application': True,
    'license': 'OEEL-1',
}
