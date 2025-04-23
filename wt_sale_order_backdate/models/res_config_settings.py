from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'


    enable_backdate_saleorder = fields.Boolean(string='Enable Backdate for Sale Order',config_parameter="wt_sale_order_backdate.enable_backdate_saleorder")
    enable_remark_saleorder = fields.Boolean(string='Enable Remark for Sale Order', config_parameter="wt_sale_order_backdate.enable_remark_saleorder")
    remark_saleorder = fields.Boolean(string='Remark Mandatory for Sale Order',config_parameter='wt_sale_order_backdate.remark_saleorder', default=False)     
    invoice_backdate = fields.Boolean(string='Invoice has Same Backdate',config_parameter ='wt_sale_order_backdate.invoice_backdate')
    delivery_backdate = fields.Boolean(string='Delivery Order has Same Backdate',config_parameter='wt_sale_order_backdate.delivery_backdate')


