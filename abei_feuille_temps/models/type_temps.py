from odoo import models, fields, exceptions, api


class TypeTemps(models.Model):
    _name = "abei_feuille_temps.type_temps"
    _description = "Permets de créer plusieurs types de saisie de temps différente."

    name = fields.Char(string="Nom", required=True)
    temps_incompressible = fields.Float(string="Temps incompressible")
    temps_unitaire = fields.Float(string="Temps unitaire", help="Test")

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
                                 string="Type de saisie de temps")

