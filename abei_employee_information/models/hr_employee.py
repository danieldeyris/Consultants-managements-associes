from odoo import fields,models


class HrEmployeePrivate(models.Model):
    _inherit = "hr.employee"

    numero_imei = fields.Char(string="N° IMEI")
    numero_pin = fields.Char(string="N° PIN")
    numero_puk = fields.Char(string="N° PUK")
    ec_inscrit = fields.Boolean(string="EC Inscrit")
