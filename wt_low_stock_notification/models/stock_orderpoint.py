from odoo import api, fields, models

from odoo import models, api


class StockWarehouseOrderpoint(models.Model):
    _inherit = 'stock.warehouse.orderpoint'
    is_low_stock = fields.Boolean(related="product_tmpl_id.is_low_stock")
    highlight_color = fields.Integer(related="product_tmpl_id.highlight_color")

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        records._recompute_product_minimum_qty()
        return records

    def write(self, vals):
        res = super().write(vals)
        self._recompute_product_minimum_qty()
        return res

    def unlink(self):
        products = self.mapped('product_id.product_tmpl_id')
        res = super().unlink()
        products._compute_minimum_quantity()
        products._compute_is_low_stock()
        products._compute_required_quantity()
        return res

    def _recompute_product_minimum_qty(self):
        """ Recompute min quantity compute for affected product templates """
        products = self.mapped('product_id.product_tmpl_id')
        if products:
            products._compute_minimum_quantity()
            products._compute_is_low_stock()
            products._compute_required_quantity()
