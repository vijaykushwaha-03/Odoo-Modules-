from odoo import models, fields, api

class AccountMove(models.Model):
    _inherit = 'account.move'

    sale_remark = fields.Char(string="Remark for Sale", compute="_compute_sale_remark")

    @api.depends('invoice_line_ids')
    def _compute_sale_remark(self):
        for move in self:
            sale_order = move.invoice_line_ids.mapped('sale_line_ids.order_id')
            move.sale_remark = sale_order[0].remark if sale_order else ''
