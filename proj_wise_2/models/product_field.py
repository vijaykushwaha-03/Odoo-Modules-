from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ProductAddField(models.Model):
    _inherit = "product.template"

    min_price = fields.Float(string="Min")
    max_price  = fields.Float(string="Max")


class SaleOrderLineSetMinMax(models.Model):
    _inherit = "sale.order.line"

    @api.onchange('price_unit')
    def _onchange_price_unit(self):
        for line in self:
            if line.product_id:
                min_price = line.product_id.min_price
                max_price = line.product_id.max_price

                # Ensure validation only runs if min_price or max_price are set AND greater than 0
                if min_price and line.price_unit < min_price:
                    raise ValidationError(
                        f"Unit price must be at least {min_price} for the product {line.product_id.name}."
                    )
                if max_price and line.price_unit > max_price:
                    raise ValidationError(
                        f"Unit price cannot exceed {max_price} for the product {line.product_id.name}."
                    )
            
        """
        Ensure unit price is within the allowed min/max range of the selected product.
        This works in the UI, but not at the database level.
        """
    
   