import base64
from odoo import models, fields, api


class ProductProduct(models.Model):
    _inherit = "product.product"

    minimum_quantity = fields.Float(string="Minimum Quantity", default=0.0)
    minimum_quantity_compute = fields.Float(
        string="Minimum Quantity Compute", compute='_compute_minimum_quantity', default=0.0)
    is_low_stock = fields.Boolean(
        string='Low Stock', compute='_compute_is_low_stock', store=True)
    required_quantity = fields.Float(
        string="Required Quantity", compute='_compute_required_quantity', default=0.0)
    highlight_color = fields.Integer(
        compute='_compute_highlight_color',
        store=False
    )

    @api.depends('is_low_stock')
    def _compute_highlight_color(self):
        for rec in self:
            if rec.is_low_stock:
                rec.highlight_color = 2
            else:
                rec.highlight_color = 0

    def _compute_minimum_quantity(self):
        config = self.env['ir.config_parameter'].sudo()
        low_stock_notification_enabled = config.get_param(
            'wt_low_stock_notification.low_stock_notification_enabled')
        product_quantity_check = config.get_param(
            'wt_low_stock_notification.product_quantity_check')
        minimum_quantity = float(config.get_param(
            'wt_low_stock_notification.minimum_quantity'))
        is_apply_on_variant = config.get_param(
            'wt_low_stock_notification.is_apply_on_variant')

        if low_stock_notification_enabled and is_apply_on_variant:
            for rec in self:
                if rec.type == 'consu':
                    if product_quantity_check == 'global':
                        rec.minimum_quantity_compute = minimum_quantity
                    elif product_quantity_check == 'individual':
                        rec.minimum_quantity_compute = rec.minimum_quantity
                    else:
                        orderpoints = self.env['stock.warehouse.orderpoint'].search(
                            [('product_id', '=', rec.id)])
                        rec.minimum_quantity_compute = min(
                            op.product_min_qty for op in orderpoints) if orderpoints else 0.0

    def _compute_required_quantity(self):
        config = self.env['ir.config_parameter'].sudo()
        low_stock_notification_enabled = config.get_param(
            'wt_low_stock_notification.low_stock_notification_enabled')
        is_apply_on_variant = config.get_param(
            'wt_low_stock_notification.is_apply_on_variant')

        if low_stock_notification_enabled and is_apply_on_variant:
            for rec in self:
                if rec.type == 'consu':
                    current_qty = rec.get_current_quantity()
                    required_quantity = rec.minimum_quantity_compute - current_qty
                    rec.required_quantity = required_quantity if required_quantity > 0 else 0

    @api.depends('qty_available', 'virtual_available', 'minimum_quantity')
    def _compute_is_low_stock(self):
        config = self.env['ir.config_parameter'].sudo()
        low_stock_notification_enabled = config.get_param(
            'wt_low_stock_notification.low_stock_notification_enabled')
        is_apply_on_variant = config.get_param(
            'wt_low_stock_notification.is_apply_on_variant')

        if low_stock_notification_enabled:
            for rec in self:
                if rec.type == 'consu' and is_apply_on_variant:
                    current_qty = rec.get_current_quantity()
                    rec.is_low_stock = current_qty <= rec.minimum_quantity_compute
                else:
                    rec.is_low_stock = False

    def get_current_quantity(self):
        config = self.env['ir.config_parameter'].sudo()
        quantity_type = config.get_param(
            'wt_low_stock_notification.quantity_type')
        return self.qty_available if quantity_type == 'onhand_qty' else self.virtual_available

    def get_low_stock_product(self):
        if self.is_low_stock_apply_on_variant():
            return self.search([
                ('is_low_stock', '=', True),
                '|',
                ('company_id', '=', self.env.company.id),
                ('company_id', '=', False)
            ])
        else:
            return self.env['product.template'].get_low_stock_product()

    def is_low_stock_apply_on_variant(self):
        config = self.env['ir.config_parameter'].sudo()
        is_apply_on_variant = config.get_param(
            'wt_low_stock_notification.is_apply_on_variant')
        return is_apply_on_variant

    def _send_low_stock_notification_email(self):
        config = self.env['ir.config_parameter'].sudo()

        mail_template = self.env.ref(
            'wt_low_stock_notification.low_stock_notification_product_product_email_template')

        low_stock_notification_enabled = config.get_param(
            'wt_low_stock_notification.low_stock_notification_enabled')

        low_stock_products = self.get_low_stock_product()
        print(">>>>>>>>>>>>>>", mail_template,
              low_stock_notification_enabled, low_stock_products)
        if mail_template and low_stock_notification_enabled and low_stock_products:

            ir_actions_report_sudo = self.env['ir.actions.report'].sudo()

            low_stock_report_action = self.env.ref(
                'wt_low_stock_notification.action_report_low_stock_product_product')

            low_stock_report = low_stock_report_action.sudo()

            content, _content_type = ir_actions_report_sudo._render_qweb_pdf(
                low_stock_report, res_ids=low_stock_products.ids)

            mail_template.attachment_ids = self.env['ir.attachment'].create({
                'name': 'Low_Stock_Products_Report.pdf',
                'type': 'binary',
                'mimetype': 'application/pdf',
                'raw': content,
                'res_model': mail_template._name,
                'res_id': mail_template.id,
            })

            mail_template.sudo().send_mail(
                self.id,
                force_send=True
            )
