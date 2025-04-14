from odoo import models, fields, api

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    disable_adding_followers_list = fields.Boolean(string="Disable auto-adding followers")

    disable_follower_option = fields.Selection([
        ('globally', 'Disable auto-adding followers globally'),
        ('chatter', 'Disable chatter to followers'),
    ], string="Disable Follower Option", default='globally')

    @api.model
    def get_config_settings_followers(self):
        disable_list = self.env['ir.config_parameter'].sudo().get_param(
            'wt_all_in_one_disable_followers.disable_adding_followers_list') == 'True'
        disable_option = self.env['ir.config_parameter'].sudo().get_param(
            'wt_all_in_one_disable_followers.disable_follower_option') == 'globally'
        return {'configDisableFollower': disable_list and disable_option}

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        ir_config = self.env['ir.config_parameter'].sudo()
        res.update(
            disable_adding_followers_list=ir_config.get_param(
                'wt_all_in_one_disable_followers.disable_adding_followers_list', default=False),
            disable_follower_option=ir_config.get_param(
                'wt_all_in_one_disable_followers.disable_follower_option', default='globally')
        )
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        ir_config = self.env['ir.config_parameter'].sudo()
        ir_config.set_param(
            'wt_all_in_one_disable_followers.disable_adding_followers_list', self.disable_adding_followers_list)
        ir_config.set_param(
            'wt_all_in_one_disable_followers.disable_follower_option', self.disable_follower_option)
