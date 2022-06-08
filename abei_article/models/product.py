from odoo import models, fields


class ProductProduct(models.Model):
    _inherit = "product.product"

    # SI UNE 'Description vente' EST DEFINIE DANS L'ARTICLE
    # ALORS LORS DE LA SELECTION DE CET ARTICLE DANS LE DEVIS
    # LA DESCRIPTION (article du devis) = DESCRIPTION VENTE (article)
    # SINON DESCRIPTION (article du devis) = LIBELLE (article)
    def get_product_multiline_description_sale(self):
        name = self.display_name
        if self.description_sale:
            name = self.description_sale
        return name
