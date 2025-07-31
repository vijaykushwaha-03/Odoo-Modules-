{
    'name': 'Announcement Bar',
    'version': '1.0',
    'category': 'Website',
    'summary': 'Customizable Announcement Bar for Website',
    'depends': ['website'],
    'data': [
        'views/layout_inherit.xml',
        'views/snippets.xml',
        'views/announcement_templates.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'announcement_bar/static/src/css/announcement_bar.css',
        ],
    },
    'installable': True,
    'application': False,
}
