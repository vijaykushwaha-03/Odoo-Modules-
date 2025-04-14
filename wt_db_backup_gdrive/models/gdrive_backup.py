# -*- coding: utf-8 -*-
# Copyright (C) Wisenetic Technologies.

import os
import json
import requests
import logging
from odoo import models

_logger = logging.getLogger(__name__)

class AutoBackup(models.Model):
    _name = 'gdrive.backup'
    _description = 'Automatic Database Backup on Google Drive'   

    # Helper function to get configuration parameters.
    def _get_config_param(self, param_name):       
        return self.env['ir.config_parameter'].sudo().get_param(param_name)
  
    def create_gdrive_backup(self):    
        local_backup_enabled = self._get_config_param('db_backup.local_backup_enabled') == 'True'  
        gdrive_backup_enabled = self._get_config_param('gdrive_db_backup.gdrive_backup_enabled') == 'True'      
        backup_format = self._get_config_param('gdrive_db_backup.backup_format')

        if not (local_backup_enabled and gdrive_backup_enabled):
            _logger.error("Either local or Google Drive backup must be enabled.")
            return False

        backup_model = self.env['db.local.backup']       
        backup_result = backup_model.perform_backup(backup_format, storage_type="gdrive")        
        backup_dir = backup_result.get("backup_dir")     

        if not backup_dir or not os.path.exists(backup_dir):
            _logger.error("Backup directory is invalid or does not exist.")
            return False

        try:
            """ Get the latest backup file """
            backup_files = sorted(
                [f for f in os.listdir(backup_dir) if f.endswith(f'.{backup_format}')],
                key=lambda x: os.path.getmtime(os.path.join(backup_dir, x)),
                reverse=True
            )            

            if not backup_files:
                _logger.error("No backup files found in the directory.")
                return False
            backup_file_path = os.path.join(backup_dir, backup_files[0])

            return self.upload_to_gdrive(backup_file_path, backup_file_path)

        except Exception as e:
            _logger.error(f"Error accessing backup files: {e}")
            return False
        
    # First-time authentication, request refresh token
    def get_refresh_token(self):        
        client_id = self._get_config_param('gdrive_db_backup.client_id')
        client_secret = self._get_config_param('gdrive_db_backup.client_secret')
        auth_code = self._get_config_param('gdrive_db_backup.authentication_code')

        if not client_id or not client_secret or not auth_code:
            _logger.error("Missing OAuth credentials for Google Drive authentication.")
            return None
        
        url = "https://oauth2.googleapis.com/token"        
        data = {
            "client_id": client_id,
            "client_secret": client_secret,
            "code": auth_code,
            "grant_type": "authorization_code",
            "redirect_uri": "http://localhost:8069/google_drive/authentication"
        }
        response = requests.post(url, data=data)
        
        if response.status_code == 200:
            token_data = response.json()
            refresh_token = token_data.get("refresh_token")

            if refresh_token:
                self.env['ir.config_parameter'].sudo().set_param('gdrive_db_backup.refresh_token', refresh_token)                
            else:
                _logger.warning("No refresh token received from Google. It might already be registered.")
        else:
            _logger.error("Failed to obtain refresh token: %s", response.json())
        
    def get_access_token(self):
        client_id = self._get_config_param('gdrive_db_backup.client_id')
        client_secret = self._get_config_param('gdrive_db_backup.client_secret')        
        refresh_token = self._get_config_param('gdrive_db_backup.refresh_token')

        # Check if required credentials exist
        if not client_id or not client_secret:
            _logger.error("Missing client credentials for access token request.")
            return None

        # Generate refresh token if missing
        if not refresh_token:
            _logger.warning("No refresh token found. Attempting to generate one.")
            self.get_refresh_token()
            refresh_token = self._get_config_param('gdrive_db_backup.refresh_token')

        if not refresh_token:
            _logger.error("Failed to obtain a refresh token.")
            return None    

        url = "https://oauth2.googleapis.com/token"
        data = {
            "client_id": client_id,
            "client_secret": client_secret,
            "refresh_token": refresh_token,
            "grant_type": "refresh_token"
        }
        response = requests.post(url, data=data)

        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data.get("access_token")

            if access_token:
                return access_token
            else:
                _logger.error("Access token missing in response.")
                return None
        else:
            _logger.error("Failed to get access token: %s", response.json())
            return None
        
    def upload_to_gdrive(self, file_path, backup_file_path):                
        """Uploads the backup file to Google Drive"""
        access_token = self.get_access_token()
        google_drive_folder_id = self._get_config_param('gdrive_db_backup.folder_id')
        notify_user = self._get_config_param('gdrive_db_backup.notify_user')
        
        if not access_token:
            _logger.error("Could not retrieve access token.")
            return False
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        metadata = {
            "name": os.path.basename(file_path),
            "parents": [google_drive_folder_id]
        }
        files = {
            'metadata': ('metadata', json.dumps(metadata), 'application/json'),
            'file': (os.path.basename(file_path), open(file_path, 'rb'), 'application/zip')
        }

        try:
            response = requests.post(
                "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",
                headers=headers,
                files=files
            )

            if response.status_code == 200:                
                file_id = response.json().get("id")                
                _logger.info(f"Backup uploaded successfully to Google Drive with file ID: {file_id}")
                
                # Remove the local backup file after successful upload
                os.remove(backup_file_path)
                # Delete old backup files from Google Drive to manage storage
                self._delete_old_files(google_drive_folder_id, headers)                
                # Send a success email notification using Odoo's email system
                if notify_user:                   
                    self.send_email_notification('wt_email_template_gdrive_backup_success', file_path=file_path, file_id=file_id)

                return file_id
            else:
                error_message = f"Google Drive upload failed: {response.text}"
                _logger.error(f"Google Drive upload failed: {response.text}")
                if notify_user:
                    self.send_email_notification('wt_email_template_gdrive_backup_fail', error_message=error_message)
                return False

        except Exception as e:
            error_message = f"Failed to upload backup: {e}"
            _logger.error(f"Failed to upload backup: {e}")
            if notify_user:
                self.send_email_notification('wt_email_template_gdrive_backup_fail', error_message=error_message)
            return False
        
    def _get_drive_files(self, folder_id, headers):
        """Fetches file list from Google Drive"""
        query = f"'{folder_id}' in parents and trashed = false"
        list_url = f"https://www.googleapis.com/drive/v3/files?q={query}&orderBy=createdTime&fields=files(id,name,createdTime)"

        try:
            response = requests.get(list_url, headers=headers)
            if response.status_code == 200:               
                return response.json().get('files', [])
            else:
                _logger.error(f"Failed to fetch file list: {response.text}")
                return []
        except Exception as e:
            _logger.error(f"Error fetching file list: {e}")
            return []

    def _delete_old_files(self, folder_id, headers):       
        files = self._get_drive_files(folder_id, headers)
        
        if len(files) > 3:           
            old_files = sorted(files, key=lambda x: x['createdTime'])[:-3]

            for file in old_files:
                delete_url = f"https://www.googleapis.com/drive/v3/files/{file['id']}"
                try:
                    delete_response = requests.delete(delete_url, headers=headers)
                    if delete_response.status_code in [200, 204]:
                        _logger.info(f"Deleted old backup file: {file['name']}")
                    else:
                        _logger.error(f"Failed to delete file {file['name']}: {delete_response.text}")
                except Exception as e:
                    _logger.error(f"Error deleting file {file['name']}: {e}")    

    def send_email_notification(self, template_xml_id, file_path=None, file_id=None, error_message=None):
        """Generic method to send success or failure email notifications"""
        template = self.env.ref(f'wt_db_backup_gdrive.{template_xml_id}')
        recipient_email = self._get_config_param('gdrive_db_backup.email_notification')
        print(recipient_email)

        if not recipient_email:
            _logger.error("Email notification is not configured. Please set an email in the config.")
            return

        if template:
            context_data = {
                'file_name': os.path.basename(file_path) if file_path else '',
                'file_id': file_id or '',
                'error_message': error_message or '',
                'recipient_email': recipient_email
            }
            mail_id = template.with_context(**context_data).send_mail(self.env.user.id, force_send=True)

            if mail_id:
                _logger.info(f"Email sent successfully (Mail ID: {mail_id})")
            else:
                _logger.error("Email sending failed.")
        else:
            _logger.error("Email template not found.")
        