from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Custom(models.Model):
    _inherit = 'sale.order'

    cash = fields.Boolean(string="Cash")
    cash_enabled = fields.Boolean(
        string="Cash Enabled in Settings",
        compute="_compute_cash_enabled",
        store=False  # Not stored in the database
    )
 
    @api.depends_context('uid')
    def _compute_cash_enabled(self):
        param_value = self.env['ir.config_parameter'].sudo().get_param('proj_wise_2.cash')
        # print("=============",param_value)
        for record in self:
            record.cash_enabled = param_value == 'True'
 
    @api.onchange('cash')
    def _onchange_cash(self):
        """
        When 'cash' is checked, remove all taxes from order lines and recalculate totals.
        """
        for order in self:
            if order.cash:
                for line in order.order_line:
                    line.tax_id = [(5, 0, 0)]  # Remove all taxes from the line
            else:
                # Restore default tax logic if cash is unchecked
                for line in order.order_line:
                    line.tax_id = line.product_id.taxes_id  # Set product default taxes

            order._amount_all()  # Recompute totals
  
    @api.depends('order_line.price_total')
    def _amount_all(self):
        """
        Custom total computation to ensure correct totals when cash is checked.
        """
        for order in self:
            amount_untaxed = sum(line.price_subtotal for line in order.order_line)
            amount_tax = sum(line.price_tax for line in order.order_line) if not order.cash else 0.0
            order.update({
                'amount_untaxed': amount_untaxed,
                'amount_tax': amount_tax,
                'amount_total': amount_untaxed + amount_tax
            })

class Connectors(models.TransientModel):
    _inherit = "res.config.settings"

    cash = fields.Boolean(string="Enable Cash Payment", default=False)

    def set_values(self):
        """
        Override set_values to save the cash setting in ir.config_parameter.
        """
        super(Connectors, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('proj_wise_2.cash', self.cash)

    @api.model
    def get_values(self):
        """
        Override get_values to retrieve the cash setting from ir.config_parameter.
        """
        res = super(Connectors, self).get_values()
        res['cash'] = self.env['ir.config_parameter'].sudo().get_param('proj_wise_2.cash', default='False') == 'True'
        # print("==========>>>",res)
        return res
        