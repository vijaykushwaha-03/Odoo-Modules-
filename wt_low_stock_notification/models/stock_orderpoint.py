from odoo import api, fields, models

class StockWarehouseOrderpoint(models.Model):
    _inherit = "stock.warehouse.orderpoint"

    alert_state = fields.Boolean(
        string='Product Alert State',
        compute='_compute_alert_state',
        store=False,
        help='Indicates if the product is in low stock based on reorder rules.'
    )

    @api.depends('product_id.qty_available', 'product_id.virtual_available', 'product_min_qty')
    def _compute_alert_state(self):
        config = self.env['ir.config_parameter'].sudo()
        stock_alert_enabled = config.get_param('wt_low_stock_notification.low_stock_alert') == 'True'
        product_quantity_check = config.get_param('wt_low_stock_notification.product_quantity_check')
        quantity_type = config.get_param('wt_low_stock_notification.quantity_type', 'onhand_qty')

        for op in self:
            op.alert_state = False

            if not stock_alert_enabled or product_quantity_check != 'reorder_rules':
                continue

            current_qty = (
                op.product_id.qty_available
                if quantity_type == 'onhand_qty'
                else op.product_id.virtual_available
            )

            if op.product_min_qty > 0 and current_qty <= op.product_min_qty:
                op.alert_state = True
