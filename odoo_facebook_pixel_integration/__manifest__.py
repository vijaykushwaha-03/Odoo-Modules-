{
    'name': 'Odoo Facebook Pixel Integration',
    'version': '18.0.0.0.1',   
    'description': """Create the custom module Odoo Facebook Pixel Integration.""",
    'depends': ['base', 'website'],
    'data': [
        'views/res_config_settings_views.xml',
        'views/website_templates_header.xml'
    ],
    'installable': True,
    'application': True,
    'auto_install': False,   
}
