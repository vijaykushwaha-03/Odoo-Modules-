from datetime import timedelta
from odoo import models, fields, api
from odoo.exceptions import UserError

class ResUsersPasswordExpiry(models.Model):
    _name = "res.users.password.expiry"
    _description = "User Password Expiry"
    _order = "user_id, id desc"

    user_id = fields.Many2one(
        'res.users',
        string="User",
        required=True,
        ondelete="cascade",
        index=True,
    )

    password_write_date = fields.Date(
        string="Last Password Update",  # <-- changed from Datetime to Date
    )

    next_password_write_date = fields.Date(
        string="Next Password Expiry",
        compute="_compute_next_password_write_date",
        store=True
    )
    _sql_constraints = [
        ('unique_user_id', 'unique(user_id)', 'Each user can only have one password expiry record.')
    ]
    @api.model
    def sync_existing_users(self):
        """Ensure all users have a password expiry record."""
        print("====================sync users=========================")
        existing_user_ids = self.sudo().search([]).mapped('user_id.id')
        users_to_sync = self.env['res.users'].search([('id', 'not in', existing_user_ids)])
        for user in users_to_sync:
            self.sudo().create({'user_id': user.id})

    @api.model_create_multi
    def create(self, vals_list):
        """Ensure password_write_date is set on creation if missing."""
        for vals in vals_list:
            if not vals.get('password_write_date'):
                vals['password_write_date'] = fields.Date.context_today(self)
        return super().create(vals_list)

    @api.depends('password_write_date')
    def _compute_next_password_write_date(self):
        """Compute next password expiry date using date only (no time)."""
        print("=====================_compute_next_password_write_date=============================")
        expiration_days = int(self.env['ir.config_parameter'].sudo().get_param(
            'auth_password_policy.password_expiration', default=90
        ))
        all_records = self.env['res.users.password.expiry'].sudo().search([])
        for rec in all_records: 
            base_date = rec.password_write_date or rec.create_date.date() if rec.create_date else False
            if base_date and expiration_days > 0:
                rec.next_password_write_date = base_date + timedelta(days=expiration_days)
            else:
                rec.next_password_write_date = False

    def action_send_expiry_reminder(self):
        """Send expiry reminder emails X days before expiration"""
        print("===================Trigger this function ==============================")
        alert_days = int(self.env['ir.config_parameter'].sudo().get_param(
            'auth_password_policy.password_expiration_alert', default=5
        ))

        today = fields.Date.context_today(self)
        target_date = today + timedelta(days=alert_days)

        users_to_notify = self.sudo().search([
            ('next_password_write_date', '=', target_date),
        ])

        mail_template = self.env.ref('wt_password_expiration.email_template_password_expiration', raise_if_not_found=False)
        if not mail_template:
            raise UserError("Password expiry mail template not found!")

        for rec in users_to_notify:
            if rec.user_id and rec.user_id.email:
                print("=========================  mail hase been send ==================")
                mail_template.send_mail(rec.user_id.id, force_send=True)