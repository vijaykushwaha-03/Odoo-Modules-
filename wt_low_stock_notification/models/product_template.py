from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = "product.template"

    minimum_product_quantity = fields.Float(string="Minimum Quantity",digits=(16, 2), store="True")
    show_minimum_qty = fields.Boolean(compute="_compute_show_minimum_qty")

    """ Low Stock Product Alert  """
    alert_state = fields.Boolean(string='Product Alert State',
                                 compute='_compute_alert_state',
                                 help='This field represents the alert state'
                                      'of the product')
    color_field = fields.Char(string='Background color',
                              help='This field represents the background '
                                   'color of the product.')

   
    @api.depends_context('company')
    def _compute_show_minimum_qty(self):
        """Show 'minimum_product_quantity' only when low_stock_alert is enabled AND product_quantity_check is 'individual'."""
        config = self.env['ir.config_parameter'].sudo()
        product_quantity_check = config.get_param('wt_low_stock_notification.product_quantity_check', '')

        for record in self:
            record.show_minimum_qty = (
                product_quantity_check == 'individual' 
            )

    @api.depends('qty_available', 'virtual_available', 'minimum_product_quantity')
    def _compute_alert_state(self):
        """Compute alert state dynamically based on selected quantity_type and config."""
        config = self.env['ir.config_parameter'].sudo()
        stock_alert_enabled = config.get_param('wt_low_stock_notification.low_stock_alert') == 'True'
        quantity_type = config.get_param('wt_low_stock_notification.quantity_type')
        product_quantity_check = config.get_param('wt_low_stock_notification.product_quantity_check')
        global_min_qty = float(config.get_param('wt_low_stock_notification.minimum_quantity', default='0'))

        for rec in self:
            rec.alert_state = False
            rec.color_field = 'white'

            if not stock_alert_enabled or rec.type != 'consu':
                continue

            # Determine current stock qty based on configuration
            current_qty = 0.0
            if quantity_type == 'onhand_qty':
                current_qty = rec.qty_available
            elif quantity_type == 'forecast_qty':
                current_qty = rec.virtual_available

            # GLOBAL: compare against global config minimum
            if product_quantity_check == 'global' and global_min_qty > 0:
                if current_qty <= global_min_qty:
                    rec.alert_state = True
                    rec.color_field = '#fdc6c673'

            # INDIVIDUAL: compare against product-specific minimum
            elif product_quantity_check == 'individual' and rec.minimum_product_quantity > 0:
                if current_qty <= rec.minimum_product_quantity:
                    rec.alert_state = True
                    rec.color_field = '#fdc6c673'
     