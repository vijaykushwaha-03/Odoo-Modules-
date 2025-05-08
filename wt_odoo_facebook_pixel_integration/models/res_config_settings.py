from odoo import models, fields

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    facebook_pixel = fields.Boolean(string="Facebook Pixel", related='website_id.facebook_pixel', readonly=False)
    pixel_tracking_id = fields.Char(string="Tracking Id", related='website_id.pixel_tracking_id', readonly=False)