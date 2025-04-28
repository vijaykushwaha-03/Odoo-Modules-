# -*- coding: utf-8 -*-
# Copyright (C) Wisenetic Technologies.
{
    'name': "Low Stock Notification",
    'summary': "Get automatic alerts and reports when product stock levels fall below minimum thresholds. [low stock notification | product stock alert | inventory stock warning | low stock email alert | stock level monitoring | product stock threshold | stock notification Odoo | product low quantity alert | Odoo inventory alert | Odoo stock notification module | inventory management Odoo | stock reorder notification | warehouse stock alert | automatic stock report | product quantity monitor | Odoo inventory automation | low stock PDF report | Odoo stock alert email | stock monitoring system]",
    'description': """Product Low Stock Notification Module for Odoo
================================================

This module helps businesses monitor product stock levels efficiently by providing automatic alerts when the stock quantity of products drops below the configured minimum threshold.

**Key Features:**
- Set global or individual minimum stock levels for products.
- Automatic calculation of required restock quantity.
- Visual low-stock indicators within product views.
- Scheduled email notifications with a PDF report of low stock products.
- Choose between 'On Hand' or 'Forecasted' quantities for checks.
- Clean, well-commented, and optimized code.
- 30-day free support included.

**Ideal for:** inventory managers, warehouse teams, procurement, and businesses seeking to prevent stockouts.

Compatible with Odoo Community and Enterprise Editions.""",
    'author': "Wisenetic",
    'website': "https://www.wisenetic.com",
    "support": "info@wisenetic.com",
    'category': "Sales/Point of Sale",
    'version': "18.0.0.0.1",
    'depends': ['base', 'mail', 'stock'],
    "data": [
        "report/ir_actions_report.xml",
        "report/low_stock_report_template.xml",
        "views/product_views.xml",
        "views/res_config_settings_views.xml",
        "views/product_template_views.xml",
        "views/stock_orderpoint_views.xml",
        "data/mail_template_data.xml",
        "data/ir_cron.xml",
    ],
    'images': ['static/description/banner.gif'],
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'OPL-1',
    'price': '5.99',
    'currency': 'USD'
}
