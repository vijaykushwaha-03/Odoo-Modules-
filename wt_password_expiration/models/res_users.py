from odoo import models, api, fields

class ResUsers(models.Model):
    _inherit = 'res.users'
    
    @api.model_create_multi
    def create(self, vals_list):
        print("========== CREATE Users ==========")
        users = super().create(vals_list)
        expiry_model = self.env['res.users.password.expiry'].sudo()
        for user in users:
            if not expiry_model.search([('user_id', '=', user.id)], limit=1):
                expiry_model.create({
                    'user_id': user.id,
                    'password_write_date': fields.Date.context_today(self),
                })
        return users

    def write(self, vals):
        print("================write Method===============")
        password_changed = 'password' in vals
        res = super().write(vals)
        expiry_model = self.env['res.users.password.expiry'].sudo()
        today = fields.Date.context_today(self)
        for user in self:
            expiry = expiry_model.search([('user_id', '=', user.id)], limit=1)
            if password_changed:
                if expiry:
                    expiry.write({'password_write_date': today})
                else:
                    expiry_model.create({
                        'user_id': user.id,
                        'password_write_date': today,
                    })
            elif not expiry:
                # fallback logic only if it doesn't already exist
                fallback_date = fields.Date.to_date(user.create_date) or today
                expiry_model.create({
                    'user_id': user.id,
                    'password_write_date': fallback_date,
                })
        return res



    # def write(self, vals):
    #     print("========== WRITE Users ==========")
    #     password_changed = 'password' in vals
    #     res = super().write(vals)
    #     if password_changed:
    #         expiry_model = self.env['res.users.password.expiry'].sudo()
    #         today = fields.Date.context_today(self)
    #         print("===============expirey_model================",expiry_model)
    #         for user in self:
    #             expiry = expiry_model.search([('user_id', '=', user.id)], limit=1)
    #             if expiry:
    #                 expiry.write({'password_write_date': today})
    #                 print("==================================",{'password_write_date': today})
    #             else:
    #                 expiry_model.create({
    #                     'user_id': user.id,
    #                     'password_write_date': today,
    #                 })
    #     return res

    # @api.model
    # def _check_credentials(self, credential, env):
    #     # First call super to verify password
    #     res = super()._check_credentials(credential, env)

    #     user = self.env.user
    #     print("========================",user.id)
    #     return res
