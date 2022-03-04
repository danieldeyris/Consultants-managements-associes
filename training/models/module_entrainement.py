import datetime

from odoo import models, fields, api, exceptions


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Une description"
    # ou ordonne directement dans la vue default_order <tree default_order="id desc">
    _order = "id desc"

    # _sql_constraints = [
    #     (
    #         'unique_account_by_transfer_model', 'UNIQUE(name)',
    #         'Le nom doit être unique'),
    #
    #     ('check_percentage', 'CHECK(percentage >= 0 AND percentage <= 100)',
    #      'The percentage of an analytic distribution should be between 0 and 100.')
    # ]

    name = fields.Char(string="Nom", required=True)
    description = fields.Char(string="Description", required=True)
    postcode = fields.Char(string="Code postal")
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string="Offre")
    expected_price = fields.Integer(string="Prix attendu", required=True)
    selling_price = fields.Float(string="Prix de vente")
    date_availability = fields.Date(string="Date de disponibilité")
    bedrooms = fields.Integer(string="Chambres")
    living_area = fields.Integer(string="Surface habitable (m²)")
    facades = fields.Integer(string="Facade")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Jardin")
    garden_area = fields.Integer(string="Surface jardin (m²)")
    garden_orientation = fields.Selection([('Nord','Nord'),('Sud','Sud'),('Est','Est'),('Ouest','Ouest')])
    total_area = fields.Char(string="Surface totale", compute="_calcul_surface")
    best_price = fields.Float(string="Meilleur prix")
    type = fields.Many2one('estate.property.type', string="Type :")
    acheteur_id = fields.Many2one("res.partner", string="Acheteur")
    vendeur_id = fields.Many2one("res.partner", string="Vendeur")
    tag = fields.Many2many('estate.property.tag', string="Tags :")
    state = fields.Selection([('Nouvelle','Nouvelle'),('OffreRecue','Offre Recue'),('OffreAcceptee','Offre Acceptee'),('Vendue','Vendue'),('Annulee','Annulee')])

    # Préférez toujours les champs calculés car ils sont également déclenchés en dehors du contexte d'une vue de formulaire.
    # N'utilisez jamais un onchange pour ajouter une logique métier à votre modèle.
    # C'est une très mauvaise idée car onchanges ne sont pas déclenchés automatiquement lors de la création d'un enregistrement par programme ; ils ne sont déclenchés que dans la vue formulaire.
    @api.onchange('garden')
    def _changement_etat_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'Est'
        else:
            self.garden_area = 0
            self.garden_orientation = ''

    @api.depends('living_area','garden_area')
    def _calcul_surface(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    # @api.depends('offer_ids.prix')
    # def _calcul_best_price(self):
    #     for record in self:
    #         res = record.value
    #         record.best_price = res

    #Bouton vue XML (Annulee)
    def action_bouton_annulee(self):
        for record in self:
            if record.state != "Vendue":
                record.state = "Annulee"
            else:
                raise exceptions.UserError("Une propriété vendue ne peut pas être annulée")
        return True

    #Bouton vue XML (Vendue)
    def action_bouton_vendue(self):
        for record in self:
            if record.state != "Annulee":
                record.state = "Vendue"
            else:
                raise exceptions.UserError("Une propriété annulée ne peut pas être vendue")
        return True

    # def _calcul_meilleur_prix(self):
    #     for record in self:
    #         for offre in record.offer_ids:
    #             if offre.status == "accepte":
    #                 record.best_price = offre.prix

    # action à la suppression (+ vérification)
    def unlink(self):
        for record in self:
            if record.state not in ['Nouvelle','Annulee']:
                raise exceptions.UserError("Il n'est pas possible de supprimer un enregistement dans un état différent de nouvelle ou annulée")
            return super().unlink()


class Type(models.Model):
    _name = "estate.property.type"
    _description = "Le type"
    _order = "name desc"

    # PERMET DE REAJOUTER LA CROIX DIRECTIONNELLE POUR CHANGER ORDRE
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")
    name = fields.Char(string="nom", required=True)
    property_ids = fields.One2many('estate.property',"type")


class Tag(models.Model):
    _name = "estate.property.tag"
    _description = "Tag"
    _order = "name desc"

    name = fields.Char(string="Tag :", required=True)


class Offer(models.Model):
    _name = "estate.property.offer"
    _description = "Une description"
    _order = "prix desc"

    prix = fields.Integer(string="Prix")
    status = fields.Selection([('accepte','Accepté'),('refuse','Refusé')])
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer(string="Période de validité (en j)", default=7)
    date_deadline = fields.Date(string="Date d'échéance", compute="_definir_dead_line", inverse="_definir_validity")

    @api.depends('validity','create_date')
    def _definir_dead_line(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + datetime.timedelta(days=record.validity)
            else:
                record.date_deadline = datetime.date.today() + datetime.timedelta(days=record.validity)


    # Les contraintes SQL sont généralement plus efficaces que les contraintes Python. Lorsque les performances comptent, préférez toujours les contraintes SQL aux contraintes Python.
    @api.constrains('date_deadline')
    def _contraite_date(self):
        for record in self:
            if record.date_deadline < fields.Date.today():
                raise exceptions.ValidationError("Une date ne peut pas être dans le passé")

    def _definir_validity(self):
        for record in self:
            date_creation = record.create_date.date()

            record.validity = (record.date_deadline - date_creation).days

    def action_confirm(self):
        for record in self:
            record.status = "accepte"
            record.property_id.best_price = record.prix
            record.property_id.acheteur_id = record.partner_id

    def action_cancel(self):
        for record in self:
            record.status = "refuse"

    # action à la création
    @api.model
    def create(self, vals):
        estate = self.env['estate.property'].browse(vals['property_id'])
        return super().create(vals)
