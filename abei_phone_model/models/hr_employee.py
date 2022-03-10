from odoo import fields,models


class HrEmployeePrivate(models.Model):
    _inherit = "hr.employee"

    phone_model = fields.Many2one("phone.model")
