from odoo import fields, models, api, exceptions


class Task(models.Model):
    _inherit = "project.task"

    @api.onchange('stage_id')
    def verification_changement_etape(self):
        # SI TACHE SELECTIONNE EST POSITIONNEE SUR UNE ETAPE OU LA SAISIE EST OBLIGATOIRE, ALORS, TRAITEMENT :
        # SAISIE TEMPS
        if self.stage_id.timesheet_mandatory:
            # SI AUCUNE LIGNE DE TEMPS N'EST SAISIE
            if self.effective_hours == 0:
                raise exceptions.UserError(
                    f"L'étape '{self.stage_id.name}' est marquée comme necessitant une saisie de temps obligatoire. \n\nHors, votre tâche '{self.name}' ne comporte aucune saisie de temps. \n\nVeuillez faire au moins une saisie de temps pour pouvoir cloturer votre tâche.")

        # SAISIE BULLETINS
        if self.stage_id.timesheet_quantity:
            somme_nombre_bulletins = 0
            for ligne_temps in self.timesheet_ids:
                somme_nombre_bulletins += ligne_temps.nombre_bulletins
            if somme_nombre_bulletins == 0:
                raise exceptions.UserError(
                    f"L'étape '{self.stage_id.name}' est marquée comme necessitant la saisie de quantité de bulletins. \n\nHors, votre tâche '{self.name}' ne comporte aucune saisie de quantité de bulletins. \n\nVeuillez faire au moins une saisie de quantité de bulletins pour pouvoir cloturer votre tâche.")
