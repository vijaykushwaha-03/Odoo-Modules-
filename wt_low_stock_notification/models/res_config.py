from odoo import api, models, fields
from odoo.exceptions import ValidationError


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    low_stock_notification_enabled = fields.Boolean(
        string="Low Stock Notification", config_parameter="wt_low_stock_notification.low_stock_notification_enabled")

    quantity_type = fields.Selection([
        ('onhand_qty', 'On Hand'),
        ('forecast_qty', 'Forecast')
    ], config_parameter="wt_low_stock_notification.quantity_type")

    product_quantity_check = fields.Selection([
        ('global', 'Global'),
        ('individual', 'Individual'),
        ('reorder_rules', 'Reorder Rules (Order Points)')
    ], config_parameter="wt_low_stock_notification.product_quantity_check")

    minimum_quantity = fields.Integer(
        string="Minimum Quantity", required=True, config_parameter="wt_low_stock_notification.minimum_quantity")

    @api.onchange('low_stock_notification_enabled')
    def _onchange_low_stock(self):
        """Clear related fields when 'low_stock' is disabled."""
        if not self.low_stock_notification_enabled:
            self.quantity_type = False
            self.product_quantity_check = False
            self.minimum_quantity = 0

    def action_open_email_template(self):
        # Find your specific template by XML ID or name
        template = self.env.ref(
            'wt_low_stock_notification.low_stock_notification_email_template')

        return {
            'type': 'ir.actions.act_window',
            'name': 'Smart Notification Email Template',
            'res_model': 'mail.template',
            'view_mode': 'form',
            'res_id': template.id,
            'target': 'new',  # or 'new' for a popup window
        }
