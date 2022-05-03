from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    # reponsables
    collaborateur_expert_comptable = fields.Many2one('hr.employee', string="Expert Comptable")
    collaborateur_principal = fields.Many2one('hr.employee', string="Collaborateur Principal")
    collaborateur_assistant_comptable = fields.Many2one('hr.employee', string="Assistant Comptable")
    collaborateur_assistant_paie = fields.Many2one('hr.employee', string="Assistant Paie")

    # collaborateurs
    collaborateur_tenue = fields.Many2one('hr.employee', string="Tenue")
    collaborateur_revision = fields.Many2one('hr.employee', string="Révision")
    collaborateur_tva = fields.Many2one('hr.employee', string="TVA")
    collaborateur_situation = fields.Many2one('hr.employee', string="Situation")
    collaborateur_divers_compta_social = fields.Many2one('hr.employee', string="Divers Compta + Social")
    collaborateur_previsionnel = fields.Many2one('hr.employee', string="Prévisionnel")
    collaborateur_flash = fields.Many2one('hr.employee', string="Flash")
    collaborateur_divers_gestion = fields.Many2one('hr.employee', string="Divers Gestion")
    collaborateur_charges_sociales = fields.Many2one('hr.employee', string="Charges Sociales")
    collaborateur_divers_social = fields.Many2one('hr.employee', string="Divers Social")
    collaborateur_paie_reguliere = fields.Many2one('hr.employee', string="Paie Régulière")
    collaborateur_paie_occasionnelle = fields.Many2one('hr.employee', string="Paie Occasionnelle")
    collaborateur_juridique = fields.Many2one('hr.employee', string="Juridique")
    collaborateur_cac = fields.Many2one('hr.employee', string="C.A.C")
    collaborateur_conseil = fields.Many2one('hr.employee', string="Conseil")

    # refClient
    # refClient = fields.Text(string="Référence client")