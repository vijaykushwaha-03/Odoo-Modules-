from odoo import models, fields

class SaleOrderBackdateWizard(models.TransientModel):
    _name = 'sale.order.backdate.wizard'
    _description = 'Assign Backdate to Quotations'

    date_order = fields.Datetime(string="Order Date", required=True)
    remark = fields.Text(string="Remarks")

    def action_confirm(self):
        orders = self.env['sale.order'].browse(self.env.context.get('active_ids', []))
        for order in orders:
            order.write({
                'date_order': self.date_order,
                'validity_date': self.date_order,
                'expected_date': self.date_order,
                'remark': self.remark,
            })
           
            for picking in order.picking_ids:
                if picking.state not in ['done', 'cancel']:
                    if 'scheduled_date' in picking._fields:
                        picking.scheduled_date = self.date_order
                    if 'date_deadline' in picking._fields:
                        picking.date_deadline = self.date_order

            
            for invoice in order.invoice_ids:
                if invoice.state not in ['posted','cancel']:
                    if 'invoice_date' in invoice._fields:
                        invoice.invoice_date = self.date_order
                    