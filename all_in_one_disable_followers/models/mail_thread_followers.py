from odoo import models, api

class MailThread(models.AbstractModel):
    _inherit = 'mail.thread'

    def general_settings(self):
        """Fetch general settings for disabling followers."""
        ir_config = self.env['ir.config_parameter'].sudo()
        return {
            'disable_followers': ir_config.get_param('wt_all_in_one_disable_followers.disable_adding_followers_list', 'False'),
            'disable_option': ir_config.get_param('wt_all_in_one_disable_followers.disable_follower_option', 'globally')
        }

    @api.model_create_multi
    def create(self, vals_list):
        """Override create method to prevent auto-followers based on config settings."""
        settings = self.general_settings()
        record = super(MailThread, self).create(vals_list)

        if settings['disable_followers'] == 'True' and settings['disable_option'] == 'globally':
            record.message_follower_ids.unlink()

        return record

    def write(self, vals):
        """Override write method to remove auto-followers if the setting is enabled."""
        settings = self.general_settings()
        result = super(MailThread, self).write(vals)

        if settings['disable_followers'] == 'True' and settings['disable_option'] == 'globally':
            for rec in self:
                # Remove all followers, even those added by email sending
                self.env['mail.followers'].sudo().search([
                    ('res_model', '=', rec._name),
                    ('res_id', '=', rec.id)
                ]).unlink()

        return result

    def message_subscribe(self, partner_ids=None, subtype_ids=None):
        """Prevent followers from being added if the setting is enabled."""
        self.ensure_one()
        settings = self.general_settings()

        # If globally disabled, prevent adding followers
        if settings['disable_followers'] == 'True' and settings['disable_option'] == 'globally':
            return  # Stop adding followers globally

        # If chatter restriction is enabled, check specific models
        if settings['disable_followers'] == 'True' and settings['disable_option'] == 'chatter':
            if hasattr(self, 'state'):
                restricted_states = self.env['manage.chatter'].get_restricted_models_states(self._name, self.env.user)
                if self.state in restricted_states:
                    return  

        return super(MailThread, self).message_subscribe(partner_ids=partner_ids, subtype_ids=subtype_ids)
