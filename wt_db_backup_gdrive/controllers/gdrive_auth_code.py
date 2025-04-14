# -*- coding: utf-8 -*-
# Copyright (C) Wisenetic Technologies.

from odoo import http
from odoo.http import request

class GoogleDriveAuth(http.Controller):
    # """Controller for handling authentication with Google Drive."""   
        
    @http.route('/google_drive/authentication', type='http', auth='user', csrf=False)
    def google_drive_auth_callback(self, **kwargs):
        
        code = kwargs.get('code')
        if not code:
            return "No authentication code received."       

        # Store the authentication code in Odoo's config parameters
        request.env['ir.config_parameter'].sudo().set_param('gdrive_db_backup.authentication_code', code)        

        return "Authentication successful. You can close this window."
