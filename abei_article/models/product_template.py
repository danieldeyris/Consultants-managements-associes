from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = "product.template"

    etiquette = fields.Many2many("project.tags", string="Etiquette")
    timesheet_mandatory = fields.Boolean("Saisie des temps obligatoire", default=False)
    timesheet_quantity = fields.Boolean("Saisie de quantités obligatoire", default=False)