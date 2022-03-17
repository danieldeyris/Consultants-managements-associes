from odoo import fields, models


class Task(models.Model):
    _inherit = "project.task"

    etiquette_projet = fields.Char(string="Etiquette Projet", readonly=True)