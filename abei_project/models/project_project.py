from odoo import fields, models


class Project(models.Model):
    _inherit = "project.project"

    etiquette_projet = fields.Many2many('project.tags', string="Etiquettes de projet")