{
    'name': 'POS Logo',
    'version': '18.0.0.0.1',   
    'description': """Create the custom module POS Logo.""",
    'depends': ['base', 'point_of_sale'],
    'data': [
        'views/res_config_settings_views.xml'
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'wt_pos_logo/static/src/**/*',
        ]
    },
    'installable': True,
    'application': True,
    'auto_install': False,   
}
