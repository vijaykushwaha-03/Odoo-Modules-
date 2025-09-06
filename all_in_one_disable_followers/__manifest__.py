{
    'name': 'All In One Disable Followers',
    'version': '18.0.0.0.1',   
    'description': """Create the custom module All in One Disable Followers.""",
    'depends': ['base', 'web', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/res_config_settings_views.xml',
        'views/manage_chatter.xml'
    ],
    'assets': {
        'web.assets_backend': [
            'wt_all_in_one_disable_followers/static/src/js/chatter_patch.js',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,   
}
