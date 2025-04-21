from odoo import models, fields

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    enable_pos_logo = fields.Boolean(string="POS Logo", related='pos_config_id.enable_pos_logo', readonly=False)
    custom_logo = fields.Binary(string="Upload Logo", related='pos_config_id.custom_logo', readonly=False)
    logo_option = fields.Selection(related='pos_config_id.logo_option', readonly=False)
