from odoo import models, fields, api

class ProductProduct(models.Model):
    _inherit = 'product.template'

    def _send_low_stock_notification_email(self, low_stock_products, product_quantity_check, global_minimum_qty):
        """Send a single email listing all low-stock products (global or individual)."""
        mail_template = self.env.ref('wt_low_stock_notification.low_stock_notification_email_template')
        if not mail_template:
            print("Email template not found!")
            return
        
        config_param = self.env['ir.config_parameter'].sudo()
        global_minimum_qty = float(config_param.get_param('wt_low_stock_notification.minimum_quantity', default=0))
        quantity_type = config_param.get_param('wt_low_stock_notification.quantity_type', default='onhand_qty')

         # Prepare dynamic message
        if product_quantity_check == 'global':
            if quantity_type == 'onhand_qty':
                alert_msg = (
                    "The following products have **on-hand stock quantity** levels "
                    "below the **global minimum quantity** configured in your system."
                )
            else:
                alert_msg = (
                    "The following products have **forecasted (virtual) stock quantity ** levels "
                    "below the **global minimum quantity** configured in your system."
                )

        elif product_quantity_check == 'individual':
            if quantity_type == 'onhand_qty':
                alert_msg = (
                    "The following products have **on-hand stock quantity ** levels "
                    "below their **individually set minimum quantity thresholds**."
                )
            else:
                alert_msg = (
                    "The following products have **forecasted (virtual) stock quantity ** levels "
                    "below their **individually set minimum quantity thresholds**."
                )

        elif product_quantity_check == 'reorder_rules':
            if quantity_type == 'onhand_qty':
                alert_msg = (
                    "The following products have **on-hand stock quantity ** levels "
                    "below the **minimum quantity defined in their Reordering Rules**."
                )
            else:
                alert_msg = (
                    "The following products have **forecasted (virtual) stock quantity ** levels "
                    "below the **minimum quantity defined in their Reordering Rules**."
                )

        product_data = []
        
        for product in low_stock_products:
            if product_quantity_check == 'individual':
                min_qty = product.minimum_product_quantity
            elif product_quantity_check == 'reorder_rules':
                orderpoint = self.env['stock.warehouse.orderpoint'].search(
                    [('product_id.product_tmpl_id', '=', product.id)], limit=1
                )
                min_qty = orderpoint.product_min_qty if orderpoint else 0
            else:  # global
                min_qty = global_minimum_qty

            product_data.append({
                'id': product.id,
                'name': product.name,
                'qty_available': product.qty_available,
                'virtual_available':product.virtual_available,
                'minimum_quantity': min_qty,
            })

        if product_data:
            mail_template.sudo().with_context(product_data=product_data,
                                              alert_message=alert_msg,
                                              quantity_type=quantity_type).send_mail(
                self.id,
                email_values={'email_to': self.env.user.email},
                force_send=True
            )
            print("Low stock notification email sent.")

    def _cron_low_stock_notification(self):
        """Cron job to send low-stock notification emails for both global and individual thresholds."""
        config_param = self.env['ir.config_parameter'].sudo()

        #  Check if alert is enabled in system config
        stock_alert_enabled = config_param.get_param('wt_low_stock_notification.low_stock_alert', default='False') == 'True'
        if not stock_alert_enabled:
            print("Low stock alert is disabled in settings. Cron skipped.")
            return

        product_quantity_check = config_param.get_param('wt_low_stock_notification.product_quantity_check')
        quantity_type = config_param.get_param('wt_low_stock_notification.quantity_type', default='onhand_qty')
        global_minimum_qty = float(config_param.get_param('wt_low_stock_notification.minimum_quantity', default=0))


        # Search all 'consumable' products
        products = self.search([('type', '=', 'consu')])
        low_stock_products = []

        for product in products:
            current_qty = product.qty_available if quantity_type == 'onhand_qty' else product.virtual_available

            # GLOBAL mode
            if product_quantity_check == 'global':
                if current_qty < global_minimum_qty:
                    product.alert_state = True
                    low_stock_products.append(product)

            # INDIVIDUAL mode
            elif product_quantity_check == 'individual':
                if product.minimum_product_quantity > 0 and current_qty < product.minimum_product_quantity:
                    product.alert_state = True
                    low_stock_products.append(product)

            # REORDER RULES logic 
            elif product_quantity_check == 'reorder_rules':
                orderpoints = self.env['stock.warehouse.orderpoint'].search([
                                    ('product_id.product_tmpl_id', '=', product.id)
                                    ])
                if orderpoints:
                    for op in orderpoints:
                        reorder_min_qty = op.product_min_qty
                        if current_qty <= reorder_min_qty:
                            product.alert_state = True
                            low_stock_products.append(product)
                             

        if low_stock_products:
            # self._send_low_stock_notification_email(low_stock_products)
            self._send_low_stock_notification_email(low_stock_products, product_quantity_check, global_minimum_qty)

        else:
            print("No products below the minimum quantity threshold. No emails sent.")