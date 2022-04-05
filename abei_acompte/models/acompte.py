from odoo import fields, models, api

PERIOD = {
    'mensuel':12,
    'bimestriel':6,
    'trimestriel':4,
    'semestriel':2,
}


class Acompte(models.Model):
    _name = "abei_acompte.acompte"
    _description = "Permet de facturer des acomptes de manière récurrente sur un devis contenant 1 ou plusieurs prestations facturées au temps passé"

    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)
    name = fields.Char(default="Numéro devis - Nom client", readonly=True)
    client = fields.Many2one("res.partner", string="Client", readonly=True)
    bon_de_commande = fields.Many2one("sale.order", string="Bon de commande", readonly=True)
    date_prochaine_facture = fields.Date(string="Date de prochaine facture")
    type_acompte = fields.Selection([('mensuel','Mensuel'),
                                     ('bimestriel','Bimestriel'),
                                     ('trimestriel','Trimestriel'),
                                     ('semestriel','Semestriel')], string="Type d'acompte")
    date_debut_acompte = fields.Date(string="Date début acompte")
    montant_a_repartir = fields.Monetary(string="Montant à répartir", currency_field="currency_id")
    acompte_line = fields.Many2many("abei_acompte.acompte.line")

    def confirm_acompte(self):
        pass

    def close_acompte(self):
        pass

    def button_client(self):
        pass

    def button_devis(self):
        pass

    def generate_acompte(self):
        for record in self:
            line_number = PERIOD[record.type_acompte]
            for i in range(line_number):
                record.acompte_line = [(0,0,{
                    'numero_acompte':i+1,
                    'libelle_acompte': f'Acompte N°{i+1} du XXXX au YYYY\r\n Lettre de mission : {record.bon_de_commande.display_name}',
                    # 'date_facture': 'XXXX',
                    'montant_acompte': record.montant_a_repartir / line_number,
                    'acompte_id': record.id
                })]


class AcompteLine(models.Model):
    _name = "abei_acompte.acompte.line"
    _description = "Une ligne d'acompte."

    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)
    numero_acompte = fields.Integer(string="N° Acompte")
    libelle_acompte = fields.Char(string="Libelle acompte")
    date_facture = fields.Date(string="Date Facture")
    montant_acompte = fields.Monetary(string="Montant de l'acompte", currency_field="currency_id")
    acompte_id = fields.Many2one("abei_acompte.acompte", required=True)


