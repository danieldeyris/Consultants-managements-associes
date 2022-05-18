from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ProjectTaskType(models.Model):
    _inherit = 'project.task.type'

    timesheet_mandatory = fields.Boolean("Saisie des temps obligatoire", default=False)
    timesheet_quantity = fields.Boolean("Saisie de quantités obligatoire", default=False)

