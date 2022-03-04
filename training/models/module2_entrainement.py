from odoo import fields, models, api


class AnnonceImmobiliere(models.Model):
    _name = "annonce.immobiliere"
    _description = "Une annonce immobiliere"

    name = fields.Char(string="Nom", required=True)
    description = fields.Text(string="Description", required=True)
    etat = fields.Selection([('bon','bon'),('moyen','moyen'),('mauvais','mauvais')], required=True)
    composition = fields.Many2many('annonce.immobiliere.composition', string="Composition")
    prix_bien = fields.Integer(string="Prix du bien", required=True)
    honoraires = fields.Integer(string="Honoraires", readonly=True, compute="_calcul_honoraires")

    @api.depends("prix_bien", "honoraires")
    def _calcul_honoraires(self):
        for record in self:
            record.honoraires = record.prix_bien * 0.1


class Composition(models.Model):
    _name = "annonce.immobiliere.composition"
    _description = "Composition du bien"

    name = fields.Char(string = "Nom", required=True)
