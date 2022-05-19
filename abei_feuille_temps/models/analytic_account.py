from odoo import models, fields, api, exceptions


class AnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    partner_id = fields.Many2one('res.partner', check_company=True, required=True)
    nombre_bulletins = fields.Integer(string="Nombre bulletins")

    # @api.onchange('nombre_bulletins')
    # def test(self):
    #     for record in self.task_id:
    #         print(record.stage_id.timesheet_mandatory)
    #         print(record.stage_id.timesheet_quantity)
    #

    # @api.model
    # def create(self, values):
    #     res = super().create(values)
    #     for record in res:
    #         # SI TACHE SELECTIONNE EST POSITIONNEE SUR UNE ETAPE OU LA SAISIE EST OBLIGATOIRE, ALORS, TRAITEMENT :
    #         # TEMPS
    #         if record.task_id.stage_id.timesheet_mandatory:
    #             # SI TEMPS NON SAISI : ERREUR
    #             if values.unit_amount == 0:
    #                 raise exceptions.UserError(
    #                     f"La saisie des heures passées est necessaire pour la tâche '{record.task_id.name}'.")
    #         # BULLETINS
    #         if record.task_id.stage_id.timesheet_quantity:
    #             # SI TEMPS NON SAISI : ERREUR
    #             if values.nombre_bulletins == 0:
    #                 raise exceptions.UserError(
    #                     f"La saisie du nombre de bulletins est necessaire pour la tâche '{record.task_id.name}'.")
    #     return res

