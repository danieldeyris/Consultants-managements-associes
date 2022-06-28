from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    chef_de_mission = fields.Many2one('hr.employee', string="Chef de mission")
    collaborateur = fields.Many2one('hr.employee', string="Collaborateur")

    @api.onchange('collaborateur')
    def _calcul_prix_collaborateur(self):
        for record in self:
            # SI AUCUN PRIX PRODUIT N'EST DEFINI (0.0) ALORS LE PRICE UNIT DEVIENT LE TAUX DE FACTU DU COLLAB.
            if record.product_id.lst_price == 0.0:
                record.price_unit = record.collaborateur.taux_facturation
            else: # SINON, LE PRICE_UNIT EST PAS DEFAUT CELUI DEFINI DANS LE PRODUIT
                record.price_unit = record.product_id.lst_price

    # OVERRIDE DE LA METHODE product_uom_change DE sale_subscription.py
    # EN CAS DE CHANGEMENT DE LA QUANTITE. SI AUCUN PRIX PRODUIT N'EST DEFINI (0.0) ALORS LE PRICE UNIT RESTE
    # LE TAUX DE FACTURATION DU COLLABORATEUR
    @api.onchange('product_uom_qty')
    def product_uom_change(self):
        res = super().product_uom_change()
        for record in self:
            if record.product_id.lst_price == 0.0:
                record.price_unit = record.collaborateur.taux_facturation
        return res


