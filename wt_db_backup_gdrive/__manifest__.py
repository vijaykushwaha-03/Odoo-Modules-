# -*- coding: utf-8 -*-
# Copyright (C) Wisenetic Technologies.

{
    'name': 'Automatic Database Backup in Google Drive',
    'summary': 'Automatic Database Backup Google Drive',
    'description': """Automatic Database Backup Google Drive""",
    'author': 'Wisenetic',
    'website': 'https://www.wisenetic.com',
    'support': 'info@wisenetic.com',
    'category': 'Extra Tools',
    'version': '18.0.0.0.1',
    'depends': ['base','mail','wt_db_backup_common'],
    'data': [   
        'security/ir.model.access.csv',        
        'data/gdrive_backup_cron.xml',
        'data/email_template.xml',
        'views/res_config_settings_views.xml',         
    ],        
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'OPL-1',   
    # 'price': '7.99',
    # 'currency': 'USD'
}