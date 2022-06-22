from odoo import fields, models, api


class Project(models.Model):
    _inherit = "project.project"

    etiquette_projet = fields.Many2many('project.tags', string="Etiquettes de projet")
    # NINOS 2
    department_user = fields.Char(related='user_id.department_id.name', readonly=True)