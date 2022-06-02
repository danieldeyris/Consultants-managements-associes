from odoo import models, fields, exceptions, api


class TypeTemps(models.Model):
    _name = "abei_feuille_temps.type_temps"
    _description = "Permets de créer plusieurs types de saisie de temps différente."

    name = fields.Char(string="Nom", required=True)
    temps_incompressible = fields.Float(string="Temps incompressible")
    temps_unitaire = fields.Float(string="Temps unitaire")

    # VALIDATION CREATION --> VERIFICATION COMPLETION DES CHAMPS
    @api.model
    def create(self, values):
        res = super().create(values)
        for record in res:
            if record.temps_incompressible == 0 and record.temps_unitaire == 0:
                raise exceptions.UserError("Les champs 'temps incompressible' et 'temps unitaire' sont vides. Veuillez en remplir au moins un.")
        return res


class ProductTemplate(models.Model):
    _inherit = "product.template"

    type_temps = fields.Many2one('abei_feuille_temps.type_temps',
                                 string="Type de saisie de temps", help="Dans le cas où l'article à des temps 'prédéfinis' (des temps connus) alors, selectionnez le type de saisie de temps.\n\n Utilité : Faciliter la saisie de temps du collaborateur (lors du transfert de tâche sur une étape de clôture, si l'article est marqué comme 'necessitant une saisie de temps obligatoire' alors Odoo se chargera de faire une saisie automatique pour l'utilisateur, en prenant pour temps de référence ceux étant indiqué dans le 'Type de saisie de temp') \n\nSi aucun type de saisie de temps n'est selectionné, alors les temps passés seront demandés au collaborateur lors du transfert de la tâche sur une étape de clôture.")
    temps_incompressible = fields.Float(string='Temps imcompressible',
                                   related='type_temps.temps_incompressible', readonly=True)
    temps_unitaire = fields.Float(string='Temps unitaire',
                                   related='type_temps.temps_unitaire', readonly=True)

