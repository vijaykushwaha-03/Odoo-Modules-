{
    "name": "Low Stock Notification",
    "author": "wisenetic",
    "license": "LGPL-3",
    "version": "1.0",
    'depends': ['base', 'stock', 'mail'],
    "data": [
        "views/product_views.xml",
        "views/res_config_settings_views.xml",
        "views/product_template_views.xml",
        # "views/stock_orderpoint_views.xml",
        "data/mail_template_data.xml",
        "data/ir_cron.xml",
    ]
}
