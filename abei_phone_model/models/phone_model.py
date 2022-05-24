from odoo import fields,models


class PhoneModel(models.Model):
    _name = "phone.model"
    _description = "Modèle du téléphone"

    name = fields.Char(string="Modèle Téléphone")