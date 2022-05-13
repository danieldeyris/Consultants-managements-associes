# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'Abeille : Quotation',
    'version': '14.0.0.0',
    'summary': 'Quotation',
    'description': """
Ce module ajoute dans les "order lines" du devis la possibilité de sélectionner le collaborateur affecté (Employee)
CAS 1 : L'article à un 'prix public' égale à 0€, alors :
- Le price_unit prend alors pour valeur le taux de facturation horaire du collaborateur.
CAS 2 : L'article à un 'prix public' supérieur à 0€, alors :
- Le price_unit reste positionné sur le prix public de l'article.

Pour le cas 1, OVERRIDE de la méthode odoo 'product_uom_change' pour régler le cas OU LE PRIX UNITAIRE REDEVENAIT LE PRIX UNITAIRE DE L'ARTICLE LORS DE LA MODIFICATION DE LA QUANTITE 
(lorsqu'il était necessaire qu'il reste positionné sur le taux horaire du collaborateur)

""",
    'author': 'Abeille',
    'website': 'https://aca-consult.com/',
    'depends': [
        'sale_management',
        'abei_employee_information',
    ],
    'data': [
        'views/sale_views.xml',
    ],
    'application': True,
    'license': 'OEEL-1',
}