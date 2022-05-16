from odoo import fields, models


class ProjectTask(models.Model):
    _inherit = 'project.task'

    color = fields.Integer('Color Index', compute="change_colore_on_kanban")

    def change_colore_on_kanban(self):
        for record in self:
            eti = 0
            for etiquette in record.tag_ids:
                eti = etiquette.color
            record.color = eti
