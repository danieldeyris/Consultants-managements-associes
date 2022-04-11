from odoo import fields, models, api


class SaleOrder(models.Model):
    _inherit = "sale.order"

    subscription_count = fields.Char(default="1")
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
                                     ('semestriel','Semestriel')], string="Type d'acompte")

    acompte_date_debut = fields.Date(string="Date de début de l'acompte")
    acompte_id = fields.Many2one("abei_acompte.acompte")

    # Lors de la sélections / désélection du la checkbox acompte
    @api.onchange('acompte_checkbox')
    def _changement_etat_acompte_checkbox(self):
        self.acompte_type = ''
        self.acompte_date_debut = ''

    def action_confirm(self):
        res = super().action_confirm()
        for sale in self:
            if sale.acompte_checkbox:
                sale.acompte_id = sale.env['abei_acompte.acompte'].create({
                    'name': f' ACOMPTE/{sale.name} - {sale.partner_id.name}',
                    'client': sale.partner_id.id,
                    'bon_de_commande': sale.id,
                    'date_prochaine_facture': sale.acompte_date_debut, # A MODIFIER
                    'type_acompte': sale.acompte_type,
                    'date_debut_acompte': sale.acompte_date_debut,
                    'millesime': sale.millesime.id,
                    'montant_a_repartir': sum(sale.order_line.filtered(
                        lambda l: not l.product_id.recurring_invoice).mapped("price_subtotal"))
                })
        return res

    def action_open_acompte(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "acompte",
            "view_mode": "form",
            "res_model": "abei_acompte.acompte",
            "res_id": self.acompte_id.id,
            "context": "{'create':False}"
        }
