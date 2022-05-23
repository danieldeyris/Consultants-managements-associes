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
    collaborateur_autre_tax_et_declaration = fields.Many2one('hr.employee', string="Aut. Tax & Decl.")
    collaborateur_previsionnel = fields.Many2one('hr.employee', string="Prévisionnel")
    collaborateur_flash = fields.Many2one('hr.employee', string="Flash")
    collaborateur_paie = fields.Many2one('hr.employee', string="Paie")
    collaborateur_charges_sociales = fields.Many2one('hr.employee', string="Charges Sociales")
    collaborateur_contrat_travail_et_m_disciplinaire = fields.Many2one('hr.employee', string="Ct. de Trav. & M. Disci.")
    collaborateur_consult_recept = fields.Many2one('hr.employee', string="Consult. recept.")
    collaborateur_juridique = fields.Many2one('hr.employee', string="Juridique")
    collaborateur_cac = fields.Many2one('hr.employee', string="C.A.C")

    # anciens collaborateurs
    ancien_collaborateur_principal = fields.Char(string="Ancien collaborateur principal")
    ancien_collaborateur_expert_comptable = fields.Char(string="Ancien collaborateur expert comptable")
    ancien_collaborateur_assistant_comptable = fields.Char(string="Ancien collaborateur assistant comptable")
    ancien_collaborateur_assistant_paie = fields.Char("Ancien collaborateur assistant paie")

    # refClient
    reCli = fields.Text(string="Référence client")