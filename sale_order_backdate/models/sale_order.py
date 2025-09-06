from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    enable_backdate_saleorder = fields.Boolean(string="Enable Backdate for Sale Order",compute="_compute_quotation_date")
    date_order = fields.Datetime(default=fields.Datetime.now)
    enable_remark_saleorder = fields.Boolean(string="Enable Remark for Sale Order",compute="_compute_remark")
    remark_saleorder = fields.Boolean(string='Remark Mandatory for sale order',compute="_compute_remark_saleorder")
    remark = fields.Char(string='Remarks')
    delivery_backdate = fields.Boolean(string='Delivery Order has Same Backdate',compute='_compute_delivery_backdate')
    invoice_backdate = fields.Boolean(string='Invoice has Same Backdate',compute='_compute_invoice_backdate')

    @api.depends()  
    def _compute_quotation_date(self):
        param_value = self.env['ir.config_parameter'].sudo().get_param('wt_sale_order_backdate.enable_backdate_saleorder', default='False')
        is_enable_backdate_saleorder = param_value.lower() == 'true'
        for record in self:
            record.enable_backdate_saleorder = is_enable_backdate_saleorder       
    
    
    @api.depends('remark')  
    def _compute_remark(self):
        param_value = self.env['ir.config_parameter'].sudo().get_param('wt_sale_order_backdate.enable_remark_saleorder', default='False')
        is_enable_remark_saleorder = param_value.lower() == 'true'
        for record in self:
            record.enable_remark_saleorder = is_enable_remark_saleorder

    @api.depends('remark')  
    def _compute_remark_saleorder(self):
        param_value = self.env['ir.config_parameter'].sudo().get_param('wt_sale_order_backdate.remark_saleorder', default='False')
        is_remark_saleorder = param_value.lower() == 'true'
        for record in self:
            record.remark_saleorder = is_remark_saleorder

    @api.depends()
    def _compute_delivery_backdate(self):
        param_value = self.env['ir.config_parameter'].sudo().get_param('wt_sale_order_backdate.delivery_backdate', default='False')
        for record in self:
            record.delivery_backdate = param_value.lower() == 'true'
    
    @api.depends()
    def _compute_invoice_backdate(self):
        param_value = self.env['ir.config_parameter'].sudo().get_param('wt_sale_order_backdate.invoice_backdate', default='False')
        for record in self:
            record.invoice_backdate = param_value.lower() == 'true'

    
    def action_confirm(self):
        for order in self:
            original_date = order.date_order if order.enable_backdate_saleorder else None
        res = super(SaleOrder, self).action_confirm()

        for order in self:
            if order.enable_backdate_saleorder and original_date:
                order.date_order = original_date

            if order.delivery_backdate:
                for picking in order.picking_ids:
                    picking.scheduled_date = order.date_order
                    picking.date_deadline = order.date_order
        return res
    
    def _prepare_invoice(self):
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        if self.date_order and self.invoice_backdate:
            invoice_vals.update({
                'invoice_date': self.date_order,
                'invoice_date_due': self.date_order,
                'date': self.date_order,
            })
        return invoice_vals
    
    def action_open_backdate_wizard(self):
        action = self.env['ir.actions.act_window']._for_xml_id(
            'wt_sale_order_backdate.action_open_backdate_wizard')
        action['context'] = {'active_ids': self.ids}
        return action
    
    
