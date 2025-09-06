{
    'name': 'Smart Alerts',
    'version': '18.0.1.0.0',
    'category': 'Extra Tools',
    'summary': 'Smart Alerts On Any Model Based on Different Conditions',
    'description': """ Admin Can create Alert configuration based on different conditions.
    With different types of Alert""",
    'author': 'Odoo custom Technology',
    'company': 'Odoo custom Technology',
    'maintainer': 'Odoo custom Technology',
    'website': 'https://www.cybrosys.com',
    'depends': ['base'],
    'uninstall_hook': 'uninstall_hook',
    'data': [
        'security/smart_alert_warning_groups.xml',
        'security/ir.model.access.csv',
        'views/alert_message_views.xml',
    ],
    'images': ['static/description/banner.jpg'],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
