from odoo import fields, models, exceptions, api, _
from dateutil.relativedelta import relativedelta
from math import *
from datetime import datetime

PERIOD = {
    'mensuel': 12,
    'bimestriel': 6,
    'trimestriel': 4,
    'semestriel': 2,
}


class Acompte(models.Model):
    _name = "abei_acompte.acompte"
    _description = "Permet de facturer des acomptes de manière récurrente sur un devis contenant 1 ou plusieurs " \
                   "prestations facturées au temps passé"
    _order = "id desc"

    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)
    name = fields.Char(readonly=True)
    client = fields.Many2one("res.partner", string="Client", readonly=True)
    bon_de_commande = fields.Many2one("sale.order", string="Bon de commande", readonly=True)
    date_prochaine_facture = fields.Date(string="Date de prochaine facture")
    type_acompte = fields.Selection([('mensuel', 'Mensuel'),
                                     ('bimestriel', 'Bimestriel'),
                                     ('trimestriel', 'Trimestriel'),
                                     ('semestriel', 'Semestriel')], string="Type d'acompte", required=True)
    date_debut_acompte = fields.Date(string="Date de début acompte", required=True)
    montant_a_repartir = fields.Monetary(string="Montant à répartir", currency_field="currency_id", required=True)
    acompte_line = fields.One2many("abei_acompte.acompte.line", "acompte_id")
    montant_total_lignes_acompte = fields.Monetary(compute='_compute_amount', string='Total', readonly=True)
    millesime = fields.Many2one("abei_millesime.millesime", readonly=True, string="Millésime")
    lignes_existantes = fields.Boolean()
    reste_a_repartir = fields.Monetary(compute='_compute_amount', string='Reste à répartir', readonly=True)
    acompte_confirme = fields.Boolean(default=False, string="Acompte confirmé")
    @api.onchange('acompte_line')
    def _compute_amount(self):
        for acompte in self:
            total = 0.0
            for line in acompte.acompte_line:
                total += line.montant_acompte
            acompte.reste_a_repartir = acompte.montant_a_repartir - total
            acompte.montant_total_lignes_acompte = total
            # S'il n'y a plus de lignes, changement état checkbox
            if len(acompte.acompte_line) == 0:
                acompte.lignes_existantes = False
            else:
                acompte.lignes_existantes = True

    def button_client(self):
        self.ensure_one()

        return {
            "type": "ir.actions.act_window",
            "name": "Client",
            "view_mode": "form",
            "res_model": "res.partner",
            "res_id": self.client.id
        }

    def button_devis(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Devis",
            "view_mode": "form",
            "res_model": "sale.order",
            "res_id": self.bon_de_commande.id
        }

    def _generate_invoice(self):
        # Si ligne d'acompte déjà facturée, n'est pas refacturée
        acompte_line_ids = self.env['abei_acompte.acompte.line'].search([(
            'date_facture', '=', datetime.today().date()
        ), (
            'est_facture', '!=', True
        ), (
            'acompte_id.acompte_confirme', '=', True
        )])

        # Recherche du produit portant le nom "Acompte" pour le downpayment
        # Alternative au passage par le res.config.settings -> Ventes -> Facturation -> Acomptes
        product_id = self.env['product.product'].search([(
            'name', '=', 'Acompte'
        )])


        #test = self.env.user.company_id
        for line in acompte_line_ids:

            order_line_id = self.env['sale.order.line'].create({
                'name': line.libelle_acompte, # Required
                'price_unit': line.montant_acompte, # Required
                'product_uom_qty': 0, # Required
                'order_id': line.acompte_id.bon_de_commande.id, # Required
                #'discount': 0.0,
                #'product_uom': self.product_id.uom_id.id,
                'product_id': product_id.id,
                #'analytic_tag_ids': analytic_tag_ids,
                'tax_id': [(6, 0, [1])], # forcé [1]
                #'tax_id': [(6, 0, tax_ids)],
                'is_downpayment': True,
                # 'qty_delivered': 0,
                # 'qty_to_invoice': -1, # ReadOnly
                # 'qty_invoiced': 1, # ReadOnly
                #'invoice_lines': ,# MANQUANT
            })

            account_move_id = self.env['account.move'].with_context(default_move_type='out_invoice').create({
                # donnees provenant de sale_make_invoice_advance (ligne 73) def _prepare_invoice_values
                # 'ref': order.client_order_ref,
                'millesime': line.acompte_id.bon_de_commande.millesime.id,
                'move_type': 'out_invoice',
                'invoice_origin': line.acompte_id.bon_de_commande.name,  # readOnly
                'invoice_user_id': line.acompte_id.bon_de_commande.user_id.id,
                'narration': line.acompte_id.bon_de_commande.note,
                'partner_id': line.acompte_id.bon_de_commande.partner_invoice_id.id,
                'fiscal_position_id': line.acompte_id.bon_de_commande.partner_id.property_account_position_id,
                'partner_shipping_id': line.acompte_id.bon_de_commande.partner_shipping_id.id,
                'currency_id': line.acompte_id.bon_de_commande.pricelist_id.currency_id.id,
                'payment_reference': line.acompte_id.bon_de_commande.reference,
                'invoice_payment_term_id': line.acompte_id.bon_de_commande.payment_term_id.id,
                'partner_bank_id': line.acompte_id.bon_de_commande.company_id.partner_id.bank_ids[:1].id,
                'team_id': line.acompte_id.bon_de_commande.team_id.id,
                'campaign_id': line.acompte_id.bon_de_commande.campaign_id.id,
                'medium_id': line.acompte_id.bon_de_commande.medium_id.id,
                'source_id': line.acompte_id.bon_de_commande.source_id.id,
                'invoice_line_ids': [(0, 0, {
                    'name': line.libelle_acompte,  # dans la facture
                    'price_unit': line.montant_acompte,
                    'quantity': 1.0,
                    'product_id': product_id.id,
                    'product_uom_id': order_line_id.product_uom.id,
                    'tax_ids': [(6, 0, order_line_id.tax_id.ids)],
                    'sale_line_ids': [(6, 0, [order_line_id.id])],
                    'analytic_tag_ids': [(6, 0, order_line_id.analytic_tag_ids.ids)],
                    'analytic_account_id': line.acompte_id.bon_de_commande.analytic_account_id.id or False,
                })]
            })

            line.acompte_id.bon_de_commande.order_line = [(4, order_line_id.id)]
            # on passe l'acompte comme facturé
            line.write({'est_facture': True})

    def generate_acompte(self):
        for record in self:
            if len(record.acompte_line) > 0:
                raise exceptions.UserError(
                    "Veuillez supprimer les lignes d'acompte actuel pour en générer de nouvelles.")
            elif record.date_prochaine_facture is False:
                raise exceptions.UserError(
                    "Veuillez selectionner une 'Date de prochaine facture'.")
            else:
                record.lignes_existantes = True
                #record.montant_total_lignes_acompte = record.montant_a_repartir
                line_number = int(PERIOD[record.type_acompte])
                # calcul du nombre de mois à ajouter à chaques lignes d'acompte
                interval = int(12 / PERIOD[record.type_acompte])
                interval_suivant = 0
                difference = 0
                nombre_lignes_condensees = 1
                nombre_mois_condenses = 1
                date_debut = record.date_debut_acompte
                # ajout de X mois et retrait de 1 jour (pour viser le dernier jour du mois précédent)
                date_fin = record.date_debut_acompte + relativedelta(months=interval) - relativedelta(days=1)
                # date facture => Dernier jour du mois saisi.
                date_facture = record.date_prochaine_facture + relativedelta(day=31)
                incremented = False
                # si date de facture hors de la premiere période d'acompte
                # si date de facture > date de début d'acompte +
                # interval en fonction du type d'acompte, alors cas spécial
                cas_particulier = False
                # 1- CAS SPECIAL - PLUSIEURES LIGNES D'ACOMPTE SONT REGROUPEES DANS UNE MEME LIGNE
                if date_facture > (date_debut + relativedelta(months=interval) - relativedelta(days=1)):
                    # flag
                    cas_particulier = True
                    # NOMBRE DE LIGNES TOTAL A AFFICHER DANS LA LISTE
                    line_number = int(line_number) - int(((date_facture.month - date_debut.month) / int(interval)))
                    # récupération de la difference de nombre de mois,
                    # pour générer une ligne d'acompte multipliant le montant de l'acompte
                    # de base par le nombre de mois que nous combinons dans une seule ligne.
                    difference = (date_facture.month - date_debut.month)

                    if record.type_acompte == "mensuel":
                        nombre_lignes_condensees = difference + 1
                        nombre_mois_condenses = nombre_lignes_condensees
                    elif record.type_acompte == "bimestriel":
                        nombre_lignes_condensees = (difference+1) / 2
                        if nombre_lignes_condensees % 2 != 0:
                            nombre_lignes_condensees = ceil(nombre_lignes_condensees)
                        nombre_mois_condenses = nombre_lignes_condensees * 2
                    elif record.type_acompte == "trimestriel":
                        nombre_lignes_condensees = (difference+1) / 3
                        if nombre_lignes_condensees % 3 != 0:
                            nombre_lignes_condensees = ceil(nombre_lignes_condensees)
                        nombre_mois_condenses = nombre_lignes_condensees * 3
                    elif record.type_acompte == "semestriel":
                        nombre_lignes_condensees = (difference+1) / 6
                        if nombre_lignes_condensees % 6 != 0:
                            nombre_lignes_condensees = ceil(nombre_lignes_condensees)
                        nombre_mois_condenses = nombre_lignes_condensees * 6

                for i in range(line_number):
                    periode = f'{date_debut.strftime("%d/%m/%Y")} au {date_fin.strftime("%d/%m/%Y")}'
                    montant_ligne_acompte = (record.montant_a_repartir / PERIOD[record.type_acompte])

                    # 1- TRAITEMENT DU CAS SPECIAL
                    # cas spécifique, combinaison de plusieurs mois pour une même ligne d'acompte (la premiere ligne)
                    if i == 0 and cas_particulier is True:
                        # MONTANT PLUSIEURES LIGNES CONDENSEES
                        montant_ligne_acompte = (record.montant_a_repartir / PERIOD[
                            record.type_acompte]) * nombre_lignes_condensees

                        # -- MENSUEL --
                        if record.type_acompte == "mensuel":
                            # modification date de début et date de fin
                            date_debut += relativedelta(months=difference)  # - relativedelta(days=1) #bon
                            date_fin = date_debut + relativedelta(months=interval) - relativedelta(days=1)
                            periode = f'{record.date_debut_acompte.strftime("%d/%m/%Y")} au {date_fin.strftime("%d/%m/%Y")}'
                        else:
                            # -- BIMESTRIEL / TRIMESTRIEL / SEMESTRIEL
                            date_debut += relativedelta(months=nombre_mois_condenses)  # - relativedelta(days=1)
                            date_fin_affichage = record.date_debut_acompte + relativedelta(months=nombre_mois_condenses) - relativedelta(days=1)
                            periode = f'{record.date_debut_acompte.strftime("%d/%m/%Y")} au {date_fin_affichage.strftime("%d/%m/%Y")}'
                            date_fin = date_debut + relativedelta(months=interval) - relativedelta(days=1)
                            incremented = True

                    # LIGNES SUIVANTES , HORS LIGNES COMBINEES
                    if i > 0:
                        # -- MENSUEL --
                        if record.type_acompte == "mensuel":
                            date_debut += relativedelta(months=interval)  # - relativedelta(days=1)
                            date_fin = date_debut + relativedelta(months=interval) - relativedelta(days=1)
                            # interval_suivant => Cumul des interval.
                            # Mensuel (1,2,3,4,5,6,7,8,9,10,11,12).
                            # Bimestriel (2,4,6,8,10,12).
                            # Trimestriel (3,6,9,12). Semestriel (6,12)
                            # permet de connaitres les differentes dates de facturation.
                            interval_suivant += interval
                            date_facture = record.date_prochaine_facture + relativedelta(
                                months=interval_suivant) + relativedelta(day=31)
                        else:
                            # -- BIMESTRIEL / TRIMESTRIEL / SEMESTRIEL
                            if incremented is not True:
                                date_debut += relativedelta(months=interval)  # - relativedelta(days=1)
                                date_fin = date_debut + relativedelta(months=interval) - relativedelta(days=1)
                            else:
                                incremented = False
                            interval_suivant += interval
                            date_facture = record.date_prochaine_facture + relativedelta(months=interval_suivant) + relativedelta(day=31)

                        # PERIODE
                        periode = f'{date_debut.strftime("%d/%m/%Y")} au {date_fin.strftime("%d/%m/%Y")}'

                    record.acompte_line = [(0, 0, {
                        'numero_acompte': i + 1,
                        'libelle_acompte': f'Acompte N°{i + 1} du {periode} \n '
                                           f'Lettre de mission : {record.bon_de_commande.display_name}',
                        'date_facture': date_facture,
                        'montant_acompte': montant_ligne_acompte,
                        'acompte_id': record.id
                    })]
                self._compute_amount()

    def confirmer_acompte(self):
        for record in self:
            if len(record.acompte_line) == 0:
                raise exceptions.UserError(
                    "L'acompte ne peut pas être confirmé, vous n'avez pas saisi de ligne d'acompte.")
        self.acompte_confirme = True

    # MODIFICATION DANS LE DEVIS DU TYPE ACOMPTE ET DE LA DATE DE DEBUT D'ACOMPTE
    def write(self, vals):
        res = super(Acompte, self).write(vals)
        for sale in self.bon_de_commande:
            if 'type_acompte' in vals:
                sale['acompte_type'] = vals['type_acompte']
            if 'date_debut_acompte' in vals:
                sale['acompte_date_debut'] = vals['date_debut_acompte']
        return res

    # A FAIRE : AVANT LA SUPRESSION, FAIRE LES VERIFICATIONS DE SECURITE, COMME SI DES FACTURES N'ON PAS ETE EMISES
    def unlink(self):
        for sale in self.bon_de_commande:
            sale['delete_from_acompte'] = True
            sale['acompte_checkbox'] = False
            sale['acompte_type'] = ''
            sale['acompte_date_debut'] = ''
        return super(Acompte, self).unlink()


class AcompteLine(models.Model):
    _name = "abei_acompte.acompte.line"
    _description = "Une ligne d'acompte."

    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)
    numero_acompte = fields.Integer(string="N° Acompte")
    libelle_acompte = fields.Char(string="Libelle acompte")
    date_facture = fields.Date(string="Date Facture")
    montant_acompte = fields.Monetary(string="Montant de l'acompte", currency_field="currency_id")
    acompte_id = fields.Many2one("abei_acompte.acompte", required=True, ondelete='cascade')
    est_facture = fields.Boolean(default=False, readonly=True, string="Ligne facturée")

    # Anti-Suppression acomptes déjà facturés
    def unlink(self):
        for record in self:
            if record.est_facture:
                raise exceptions.UserError(
                    f"La ligne d'accompte suivante : \"{record.libelle_acompte} \" n'est pas supprimable.\n\n Elle fait déjà l'objet d'une facturation ({record.acompte_id.bon_de_commande.name})")
        return super().unlink()

    # Anti-Suppression acomptes déjà facturés
    def write(self, vals):
        res = super(AcompteLine, self).write(vals)
        for record in self:
            if record.est_facture:
                if 'est_facture' not in vals:
                    raise exceptions.UserError(
                        f"La ligne d'accompte suivante : \"{record.libelle_acompte} \" n'est pas modifiable.\n\n Elle fait déjà l'objet d'une facturation ({record.acompte_id.bon_de_commande.name})")
        return res

