from dateutil.relativedelta import relativedelta

from odoo import fields, models, _, api
from odoo.tools import format_date

PERIODS = {'daily': 'days', 'weekly': 'weeks', 'monthly': 'months', 'yearly': 'years'}


class SaleSubscription(models.Model):
    _inherit = "sale.subscription"

    last_invoiced_date = fields.Date(copy=False)

    def _prepare_invoice_data(self):
        res = super()._prepare_invoice_data()
        res['subscription_id'] = self.id
        # Champ : Date de début
        next_date = self.last_invoiced_date or self.date_start
        # Ancienne date de facture (self.recurring_next_date)
        self.last_invoiced_date = self.recurring_next_date + relativedelta(days=1)
        end_date = self.recurring_next_date
        res['narration'] = _("This invoice covers the following period: %s - %s") % (format_date(self.env, next_date), format_date(self.env, end_date))

        # GESTION DATE ECHEANCE - DEBUT -
        # Présence d'une "Conditions de paiement par défaut" ?
        if res['invoice_payment_term_id']:
            # SI OUI RECUPERATION DU NOMBRE DE JOURS A AJOUTER A NOTRE DATE
            for record in self.env['account.payment.term'].browse(res['invoice_payment_term_id']):
                for line_ids in record.line_ids:
                    print(line_ids.days)
                    res['invoice_date_due'] = self.recurring_next_date + relativedelta(days=line_ids.days)
        else:
            res['invoice_date_due'] = self.recurring_next_date
        # GESTION DATE ECHEANCE - FIN -

        return res

    # RETRAIT DE DEUX LIGNES (block if) (53 & 56) qui empêchent le bon fonctionnement des dates
    # (recurring_next_date positionné sur la date du 30 alors qu'il devrait être à 31 si la premiere période d'abonnement est sur un mois se finissant en 30)
    # ex: (Abonnement mensuel du 01.06.2022 au 30.06.2022 - Premier abonnement ok, mais le suivant sera du 01.07.2022 au 30.07.2022 au lieu du 31)
    @api.model
    def _get_recurring_next_date(self, interval_type, interval, current_date, recurring_invoice_day):
        """
        This method is used for calculating next invoice date for a subscription
        :params interval_type: type of interval i.e. yearly, monthly, weekly etc.
        :params interval: number of interval i.e. 2 week, 1 month, 6 month, 1 year etc.
        :params current_date: date from which next invoice date is to be calculated
        :params recurring_invoice_day: day on which next invoice is to be generated in future
        :returns: date on which invoice will be generated
        """
        interval_type = PERIODS[interval_type]
        recurring_next_date = fields.Date.from_string(current_date) + relativedelta(**{interval_type: interval})
        if interval_type == 'months':
            last_day_of_month = recurring_next_date + relativedelta(day=31)
            # if last_day_of_month.day >= recurring_invoice_day:
            # #     # In cases where the next month does not have same day as of previous recurrent invoice date, we set the last date of next month
            # #     # Example: current_date is 31st January then next date will be 28/29th February
            #     return recurring_next_date.replace(day=recurring_invoice_day)
            # In cases where the subscription was created on the last day of a particular month then it should stick to last day for all recurrent monthly invoices
            # Example: 31st January, 28th February, 31st March, 30 April and so on.
            return last_day_of_month
        # Return the next day after adding interval
        return recurring_next_date