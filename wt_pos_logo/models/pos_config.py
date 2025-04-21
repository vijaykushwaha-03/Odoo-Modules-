from odoo import models, fields

class PosConfig(models.Model):
    _inherit = 'pos.config'

    enable_pos_logo = fields.Boolean(string="POS Logo")
    custom_logo = fields.Binary(string="Upload Logo")

    logo_option = fields.Selection([
        ('company', 'Company'),
        ('custom', 'Custom Image'),
    ], string="Disable POS Logo Option", default='company')
   