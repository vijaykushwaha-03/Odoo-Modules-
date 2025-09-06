# -*- coding: utf-8 -*-
# Copyright (C) Odoo custom Technologies.

import werkzeug.urls as urls
from odoo import models, fields, api
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    gdrive_backup_enabled = fields.Boolean(
        string = "Enable Google drive Backup",
        config_parameter='gdrive_db_backup.gdrive_backup_enabled'
    )
    gdrive_backup_frequency = fields.Selection([        
        ('days', 'Days'),
        ('weeks', 'Weeks'),
        ('months', 'Months')
    ], string="GDrive Backup Frequency", config_parameter='gdrive_db_backup.backup_frequency', default='days')
    notify_user = fields.Boolean(string='Notify User', config_parameter='gdrive_db_backup.notify_user')
    email_notification = fields.Char(string="Notification Email", config_parameter="gdrive_db_backup.email_notification")    
    gdrive_backup_time = fields.Datetime(
        string="GDrive Backup Time",
        config_parameter='gdrive_db_backup.backup_time',
        help="Set the date and time for the next scheduled backup."
    )
    gdrive_backup_format = fields.Selection([
        ('dump', 'Dump (.dump)'),
        ('zip', 'Compressed Zip (.zip)')
    ], string="GDrive Backup Format", config_parameter='gdrive_db_backup.backup_format', default='zip',
    help="Select the format for the database backup file.")
    gdrive_client_id = fields.Char(
        string="Google Client ID",
        config_parameter='gdrive_db_backup.client_id',
        help="Enter the Google API Client ID"
    )
    gdrive_client_secret = fields.Char(
        string="Google Client Secret",
        config_parameter='gdrive_db_backup.client_secret',
        help="Enter the Google API Client Secret"
    )
    gdrive_authentication_code = fields.Char(
        string="Google Authentication Code",
        config_parameter='gdrive_db_backup.authentication_code',
        help="Enter the one-time authentication code for OAuth 2.0"        
    )
    gdrive_folder_id = fields.Char(
        string="Google Drive Folder Id",
        config_parameter='gdrive_db_backup.folder_id',
        help="Enter the Google Drive Folder ID where backups will be stored."
    )
    gdrive_refresh_token = fields.Char(
        string="Google Refresh Token",
        config_parameter='gdrive_db_backup.refresh_token',
        help="Stores the refresh token to generate new access tokens"
    )      
    base_url_display = fields.Char(string='Base URL', readonly=True)

    @api.model
    def get_values(self):
        res = super().get_values()
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        res.update({
            'base_url_display': f"{base_url}/google_drive/authentication"
        })
        return res

    def action_get_gdrive_auth_code(self):
        if not self.gdrive_client_id or not self.gdrive_client_secret:
            raise ValidationError("Google Client ID and Client Secret are required before authentication.")               
        
        GOOGLE_AUTH_ENDPOINT = "https://accounts.google.com/o/oauth2/auth"
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')        
        redirect_uri = f"{base_url}/google_drive/authentication"

        # Validate required values
        if not self.gdrive_client_id or not base_url:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Error',
                    'message': 'Google Drive Client ID or Base URL is missing.',
                    'sticky': False,
                    'type': 'danger',
                },
            }
        params = {
            'client_id': self.gdrive_client_id,
            'redirect_uri': redirect_uri,
            'response_type': 'code',
            'scope': 'https://www.googleapis.com/auth/drive.file',
            'access_type': 'offline',
            'prompt': 'consent',
        }        
        auth_url = f"{GOOGLE_AUTH_ENDPOINT}?{urls.url_encode(params)}"        
        return {
            'type': 'ir.actions.act_url',
            'url': auth_url,
            'target': 'new',
    }
    
    # Method to update configuration values and modify cron job settings
    def set_values(self):         
        env = self.env['ir.config_parameter'].sudo()

        # Get previous values of client_id and client_secret
        old_client_id = env.get_param('gdrive_db_backup.client_id')
        old_client_secret = env.get_param('gdrive_db_backup.client_secret')
        super().set_values()

         # Compare old and new values
        if (old_client_id != self.gdrive_client_id) or (old_client_secret != self.gdrive_client_secret):
            env.set_param('gdrive_db_backup.authentication_code', '')
            env.set_param('gdrive_db_backup.refresh_token', '')
               
        cron = self.env.ref('wt_db_backup_gdrive.wt_gdrive_db_backup_cron', raise_if_not_found=False)
        
        if cron:
            backup_time = env.get_param('gdrive_db_backup.backup_time', False)
            if backup_time:
                nextcall = fields.Datetime.to_datetime(backup_time)
            else:
                nextcall = datetime.now() + timedelta(days=1)
                nextcall = nextcall.replace(hour=0, minute=1, second=0)

            cron.sudo().write({
                'interval_type': env.get_param('gdrive_db_backup.backup_frequency', 'days'),
                'nextcall': nextcall,
            })
    