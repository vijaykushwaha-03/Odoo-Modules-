from email.policy import default
from odoo import api, models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    low_stock_notification_enabled = fields.Boolean(
        string="Low Stock Notification", config_parameter="wt_low_stock_notification.low_stock_notification_enabled", default=False)

    quantity_type = fields.Selection([
        ('onhand_qty', 'On Hand'),
        ('forecast_qty', 'Forecast')
    ], config_parameter="wt_low_stock_notification.quantity_type", default="onhand_qty")

    product_quantity_check = fields.Selection([
        ('global', 'Global'),
        ('individual', 'Individual'),
        ('reorder_rules', 'Reorder Rules (Order Points)')
    ], config_parameter="wt_low_stock_notification.product_quantity_check", default="global")

    minimum_quantity = fields.Float(
        string="Minimum Quantity", required=True, config_parameter="wt_low_stock_notification.minimum_quantity", default=0.0)

    is_apply_on_variant = fields.Boolean(
        string="Apply On Product Variant", required=True, config_parameter="wt_low_stock_notification.is_apply_on_variant", default=False)

    def set_values(self):
        res = super().set_values()
        # Force recompute of product.template fields
        self.env['product.template'].search([])._compute_minimum_quantity()
        self.env['product.template'].search([])._compute_is_low_stock()
        self.env['product.template'].search([])._compute_required_quantity()
        self.env['product.product'].search([])._compute_minimum_quantity()
        self.env['product.product'].search([])._compute_is_low_stock()
        self.env['product.product'].search([])._compute_required_quantity()

        return res

    @api.onchange('low_stock_notification_enabled')
    def _onchange_low_stock_notification_enabled(self):
        """Clear related fields when 'low_stock' is disabled."""
        if not self.low_stock_notification_enabled:
            self.quantity_type = False
            self.product_quantity_check = False
            self.minimum_quantity = 0

    def action_open_email_template(self):
        # Find your specific template by XML ID or name
        template = self.env.ref(
            'wt_low_stock_notification.low_stock_notification_product_product_email_template')

        return {
            'type': 'ir.actions.act_window',
            'name': 'Smart Notification Email Template',
            'res_model': 'mail.template',
            'view_mode': 'form',
            'res_id': template.id,
            'target': 'new',  # or 'new' for a popup window
        }
