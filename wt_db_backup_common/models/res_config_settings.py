# -*- coding: utf-8 -*-
# Copyright (C) Wisenetic Technologies.

from odoo import fields, models
from datetime import datetime, timedelta

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    local_backup_enabled = fields.Boolean(
        string="Enable Local Backup",
        config_parameter='db_backup.local_backup_enabled'
    )
    local_backup_path = fields.Char(
        string="Backup Directory Path",
        config_parameter='db_backup.local_backup_path',
        help="Specify the directory where local backups will be stored. "
             "For example, '/home/odoo/backups'. "        
    )
    backup_frequency = fields.Selection([
        ('minutes', 'Minutes'),
        ('hours', 'Hours'),
        ('days', 'Days'),
        ('weeks', 'Weeks'),
        ('months', 'Months')
    ], string="Backup Frequency", config_parameter='db_backup.backup_frequency', default='days')
    backup_time = fields.Datetime(
        string="Backup Time",
        config_parameter='db_backup.backup_time',
        help="Set the date and time for the next scheduled backup."
    )
    backup_format = fields.Selection([
        ('dump', 'Dump (.dump)'),
        ('zip', 'Compressed Zip (.zip)')
    ], string="Backup Format", config_parameter='db_backup.backup_format', default='zip',
    help="Select the format for the database backup file.")

    # Method to update configuration values and modify cron job settings
    def set_values(self):             
        super().set_values()
        env = self.env['ir.config_parameter'].sudo()       
        cron = self.env.ref('wt_db_backup_common.wt_scheduled_local_db_backup_cron', raise_if_not_found=False)
        
        if cron:
            backup_time = env.get_param('db_backup.backup_time', False)
            if backup_time:
                nextcall = fields.Datetime.to_datetime(backup_time)
            else:
                nextcall = datetime.now() + timedelta(days=1)
                nextcall = nextcall.replace(hour=0, minute=1, second=0)

            cron.sudo().write({
                'interval_type': env.get_param('db_backup.backup_frequency', 'days'),
                'nextcall': nextcall,
            })
    