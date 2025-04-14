# -*- coding: utf-8 -*-
# Copyright (C) Wisenetic Technologies.

{
    'name': 'Automatic Database Backup in Local',
    'summary': 'Automatic Database Backup',
    'description': """Automatic Database Backup""",
    'author': 'Wisenetic',
    'website': 'https://www.wisenetic.com',
    'support': 'info@wisenetic.com',
    'category': 'Extra Tools',
    'version': '18.0.0.0.1',
    'depends': ['base','mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/auto_db_backup_cron.xml',
        'views/res_config_settings_views.xml',         
    ],    
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'OPL-1',
    'images': ['static/description/icon.png'],
    # 'price': '7.99',
    # 'currency': 'USD'
}