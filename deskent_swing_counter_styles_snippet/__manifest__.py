{
    'name': "Swing Counter style snippet",

    'summary': """
        The counters can be effortlessly added to any website page using Odoo’s drag-and-drop snippet editor, making it user-friendly for non-technical users to enhance their web pages with animated counters.
    """,

    'description': """
        Add the  diffrent snippets block 
    """,

    "author": "Devendra kavthekar",
    "support": "dkatodoo@gmail.com",
    "website": "https://dek-odoo.github.io",
    'category': 'website',
    "license": "OPL-1",
    'version': '18.0',
    "images": ["static/description/banner.gif"],
    "price": 0.00,
    "currency": "EUR",

    'depends': ['base', 'website'],

    'data': [ 
        'views/templates.xml',
    ], 
    'assets': {
        'web.assets_frontend': [
            'deskent_swing_counter_styles_snippet/static/src/css/deskent_swing_counter_styles_snippet.css',
            'deskent_swing_counter_styles_snippet/static/src/js/deskent_swing_counter_styles_snippet.js',
        ],
    },
    'application': False,
    'installable': True,
}
