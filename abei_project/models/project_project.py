from odoo import fields, models, api


class Project(models.Model):
    _inherit = "project.project"

    etiquette_projet = fields.Many2many('project.tags', string="Etiquettes de projet")
    department_user = fields.Char(related='user_id.department_id.name', readonly=True)
    my_specialization = fields.Boolean(compute="_compute_my_specialization", search="_search_my_specialization")

    def _compute_my_specialization(self):
        for rec in self:
            rec.my_specialization = False

    def _search_my_specialization(self, operator, value):
        my_tags = self.env.user.my_tags_ids
        my_projects = self.env['project.project'].search([('etiquette_projet', 'in', my_tags.ids)])
        return [('id', 'in', my_projects.ids)]


class Users(models.Model):
    _inherit = "res.users"

    my_tags_ids = fields.Many2many('project.tags')


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    user_tags_ids = fields.Many2many("project.tags", related="user_id.my_tags_ids", readonly=False)