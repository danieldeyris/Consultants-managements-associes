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

    @api.model
    def create(self, values):
        res = super().create(values)
        for record in res:
            # SI PRESENCE DE BULLETIN DANS LA LIGNE, FACTURATION
            if record.nombre_bulletins > 0:
                product_id = self.env['product.template'].search([(
                    'name', '=', 'Bulletin de Salaire'
                )])
                order = record.task_id.sale_order_id
                if order.id:
                    taxes = product_id.taxes_id.filtered(lambda r: r.company_id == order.company_id)

                    self.env['sale.order.line'].create({
                        'name': "Bulletin de salaire",
                        'price_unit': product_id.list_price,
                        'product_uom_qty': record.nombre_bulletins,
                        'order_id': order.id,
                        'product_id': product_id.id,
                        'tax_id': [(6, 0, taxes.ids)],
                        'qty_delivered': record.nombre_bulletins,
                        'ligne_saisie_temps_id': record.id,
                    })
                else:
                    raise exceptions.UserError(f"La tâche n'est rattachée à aucun devis. Les bulletins ne sont pas facturables.")
        return res

    def write(self, vals):
        res = super().write(vals)
        # NOMBRE DE BULLETINS CHANGE DANS LA LIGNE DE SAISIE DE TEMPS ==> MISE A JOUR DU DEVIS CLIENT
        if 'nombre_bulletins' in vals:
            order = self.task_id.sale_order_id
            for record in order:
                for order_line in record.order_line:
                    if order_line.ligne_saisie_temps_id == self.id:
                        order_line['product_uom_qty'] = vals['nombre_bulletins']
                        order_line['qty_delivered'] = vals['nombre_bulletins']
        return res


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    ligne_saisie_temps_id = fields.Integer()
