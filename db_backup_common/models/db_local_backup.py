# -*- coding: utf-8 -*-
# Copyright (C) Odoo custom Technologies.

import os
import logging
import datetime
import glob
import odoo
from odoo import models, http

_logger = logging.getLogger(__name__)

class AutoBackup(models.Model):
    _name = 'db.local.backup'
    _description = 'Automatic Database Backup to Local Storage'

    def _get_config_param(self):        
        Param = self.env['ir.config_parameter'].sudo()
        local_backup_enabled = Param.get_param('db_backup.local_backup_enabled', 'False') == 'True'
        local_backup_path = Param.get_param('db_backup.local_backup_path')
        backup_format = Param.get_param('db_backup.backup_format', 'zip')

        return local_backup_enabled, local_backup_path, backup_format
    
    def perform_backup(self, backup_format, storage_type):        
        """ Performs the database backup."""        
        _, local_backup_path, _ = self._get_config_param()
        db_name = self.env.cr.dbname
        backup_dir = local_backup_path if local_backup_path else os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "db_backup"
        )
       
        # Ensure backup_dir is valid
        if not backup_dir or not isinstance(backup_dir, str):
            return {"success": False, "message": "Invalid backup directory path"}

        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir, exist_ok=True)

        if storage_type != "local":
            backup_dir = os.path.join(backup_dir, "temp")
            if not os.path.exists(backup_dir):
                os.makedirs(backup_dir, exist_ok=True)             

        try:
            odoo.service.db.check_super('odoo')
            if db_name not in http.db_list():
                raise Exception("Database %r is not known" % db_name)
            
            ts = datetime.datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"{db_name}_{ts}.{backup_format}"
            file_path = os.path.join(backup_dir, filename)            
            dump_stream = odoo.service.db.dump_db(db_name, None, backup_format)
            
            with open(file_path, "wb") as f:
                f.write(dump_stream.read())        

            if storage_type == "local":
                self.cleanup_old_backups(backup_dir, db_name)

            return {"success": True, "message": f"Backup saved at {file_path}", "backup_dir": backup_dir}

        except Exception as e:
            _logger.exception("Database backup error")
            error = f"Database backup error: {str(e) or repr(e)}"
            return {"success": False, "message": error} 
    
    def create_backup(self):
        local_backup_enabled, _, backup_format = self._get_config_param()        
        if not local_backup_enabled:
            return        
        self.perform_backup(backup_format, storage_type='local')             
    
    def cleanup_old_backups(self, backup_dir, db_name):         
        backup_files = sorted(
            glob.glob(os.path.join(backup_dir, f"{db_name}_*")),
            key=os.path.getmtime,  
            reverse=True
        )
       
        for old_file in backup_files[3:]:
            try:
                os.remove(old_file)                
            except Exception as e:
                pass
