from odoo import models, fields

class PosConfig(models.Model):
    _inherit = 'website'

    facebook_pixel = fields.Boolean(string="Facebook Pixel")
    pixel_tracking_id = fields.Char(string="Tracking Id")