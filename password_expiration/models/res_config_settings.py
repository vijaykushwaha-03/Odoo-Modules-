from odoo import fields, models, api,_
from odoo.exceptions import ValidationError

class ResConfigSettings(models.TransientModel):

    _inherit = 'res.config.settings'
    
    password_expiration = fields.Integer(
        string="Password Expiration Period (days)", 
        config_parameter="auth_password_policy.password_expiration", 
        default=90,
        store=True
    )
    password_expiration_alert = fields.Integer(
        string="Expiration Alert Period (days)", 
        config_parameter="auth_password_policy.password_expiration_alert", 
        default=5
    )
    # password_minimum_length = fields.Integer(
    #     string="Minimum Password Length",
    #     config_parameter="auth_password_policy.password_minimum_length",
    #     default=8
    # )
    
    password_lower = fields.Integer(
        string="Lowercase Characters",
        config_parameter="auth_password_policy.password_lower",
        default=2
    )
    password_upper = fields.Integer(
        string="Uppercase Characters",
        config_parameter="auth_password_policy.password_upper",
        default=2
    )
    password_numeric = fields.Integer(
        string="Numeric Characters",
        config_parameter="auth_password_policy.password_numeric",
        default=2
    )
    password_special = fields.Integer(
        string="Special Characters",
        config_parameter="auth_password_policy.password_special",
        default=2
    )

    def set_values(self):
        # print("========== SET VALUES ==========")
        # Fetch old value before it was overwritten
        old_val = int(self.env['ir.config_parameter'].sudo().get_param(
            'auth_password_policy.password_expiration', default=90
        ))
        super_result = super().set_values()
        new_val = self.password_expiration
        # print(f"Old Password Expiration: {old_val}, New Password Expiration: {new_val}")
        if old_val != new_val:
            # print(f"Password expiration changed from {old_val} to {new_val} days.")
            self.env['res.users.password.expiry'].sudo()._compute_next_password_write_date()

        return super_result