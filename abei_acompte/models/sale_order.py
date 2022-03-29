from odoo import fields, models, api


class SaleOrder(models.Model):
    _inherit = "sale.order"

    # Une case à cocher permet d’indiquer que la commande est soumise à acompte
    acompte_checkbox = fields.Boolean(string="Géré par acompte")

    # Le type d’acompte permet d’indiquer la fréquence d’émission des factures d’acompte
    # Mensuel (tous les mois)
    # Bimestriel (tous les 2 mois)
    # Trimestriel (tous les 3 mois)
    # Semestriel (tous les 6 mois)
    acompte_type = fields.Selection([('mensuel','Mensuel'),
                                     ('bimestriel','Bimestriel'),
                                     ('trimestriel','Trimestriel'),
                                     ('semestriel','Semestriel')])

    acompte_date_debut = fields.Date()

    # Lors de la sélections / désélection du la checkbox acompte
    @api.onchange('acompte_checkbox')
    def _changement_etat_acompte_checkbox(self):
        if self.acompte_checkbox:
            self.acompte_type = ''
            self.acompte_date_debut = ''
        else:
            self.acompte_type = ''
            self.acompte_date_debut = ''

    # def _prepare_invoice(self):
    #     res = super()._prepare_invoice()
    #     res['acompte_checkbox'] = self.acompte_checkbox
    #     res['acompte_type'] = self.acompte_type
    #     res['acompte_date_debut'] = self.acompte_date_debut
    #     return res
