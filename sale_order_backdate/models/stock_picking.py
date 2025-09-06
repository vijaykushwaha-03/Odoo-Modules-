from odoo import models, fields

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    sale_id = fields.Many2one('sale.order') 
    sale_remark = fields.Char(
        string="Remarks for Sale",
        related='sale_id.remark',
        store=False,
        readonly=True,
    )

