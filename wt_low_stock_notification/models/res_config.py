from odoo import api , models, fields
from odoo.exceptions import ValidationError

class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    low_stock_alert = fields.Boolean(string="Low Stock Notification" ,config_parameter="wt_low_stock_notification.low_stock_alert")

    quantity_type = fields.Selection([
            ('onhand_qty', 'On Hand'),
            ('forecast_qty', 'Forecast')
        ],config_parameter="wt_low_stock_notification.quantity_type")
    
    product_quantity_check = fields.Selection([
        ('global', 'Global'),
        ('individual','Individual'),
        ('reorder_rules','Reorder Rules (Order Points)')
    ],config_parameter="wt_low_stock_notification.product_quantity_check")

    minimum_quantity = fields.Integer(string="Minimum Quantity", store=True,required=True ,config_parameter="wt_low_stock_notification.minimum_quantity" )
    show_minimum_quantity = fields.Boolean(compute="_compute_show_minimum_quantity", store=False)
     
    @api.model
    def set_values(self):
        super().set_values()

        config = self.env['ir.config_parameter'].sudo()
        low_stock_alert = self.low_stock_alert
        quantity_mode = self.product_quantity_check
                                                                        
        # Reset global minimum if not in global mode or alerts are disabled
        if not low_stock_alert or quantity_mode != 'global':
            config.set_param('wt_low_stock_notification.minimum_quantity', 0)

        # Reset all product-level minimums if not in individual mode or alerts are disabled
        if not low_stock_alert or quantity_mode != 'individual':
            products = self.env['product.template'].search([('minimum_product_quantity', '!=', 0)])
            products.write({
                'minimum_product_quantity': 0,
                'alert_state': False,
                'color_field': 'white',
            })


    @api.depends('product_quantity_check')
    def _compute_show_minimum_quantity(self):
        """Show minimum_quantity only when product_quantity_check is 'global'."""
        for record in self:
            record.show_minimum_quantity = record.product_quantity_check == 'global'

    @api.onchange('low_stock_alert')
    def _onchange_low_stock(self):
        """Clear related fields when 'low_stock' is disabled."""
        if not self.low_stock_alert:
            self.quantity_type = False
            self.product_quantity_check = False
            self.minimum_quantity = 0
    

    @api.constrains('quantity_type', 'product_quantity_check')
    def _check_quantity_type_and_product_check_required(self):
        for rec in self:
            # Condition 1: If one is selected, the other must be selected
            if rec.quantity_type and not rec.product_quantity_check:
                raise ValidationError(
                    "You must select a 'Product Quantity Check' when 'Quantity Type' is selected."
                )
            if rec.product_quantity_check and not rec.quantity_type:
                raise ValidationError(
                    "You must select a 'Quantity Type' when 'Product Quantity Check' is selected."
                )
            
             # Condition 2: Low stock toggle validation
            if rec.low_stock_alert and (not rec.quantity_type or not rec.product_quantity_check):
                raise ValidationError(
                    "To enable 'Low Stock Notification', both 'Quantity Type' and 'Product Quantity Check' must be selected."
                )
            
             # Condition 3: If global is selected, minimum_quantity must be > 0
            if rec.product_quantity_check == 'global' and rec.minimum_quantity <= 0:
                raise ValidationError(
                    "When you selected Product Quantity Check = 'Global' , you must set a 'Minimum Quantity' "
                )