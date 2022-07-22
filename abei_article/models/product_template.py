from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = "product.template"
    _order = "numerotation"

    etiquette = fields.Many2many("project.tags", string="Etiquettes")
    timesheet_mandatory = fields.Boolean("Saisie des temps obligatoire", default=False)
    timesheet_quantity = fields.Boolean("Saisie de quantités obligatoire", default=False)
    numerotation = fields.Char("Numérotation", required=True)
    type_bulletin_de_salaire = fields.Boolean(string="Type bulletin de salaire")