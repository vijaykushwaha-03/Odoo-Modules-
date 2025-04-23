{
    'name': 'Sale Order Backdate',
    'version': '1.0', 
    'license': 'LGPL-3',  
    'description': """This is a simple example module for Sale Order Backdate.""",
    'depends': ['base','sale','stock','account'],
    'data': [        
        'security/ir.model.access.csv',
        'security/groups.xml',
        'views/res_config_settings.xml',
        'views/account_move.xml',
        'views/stock_picking.xml',
        'wizard/sale_order_backdate_wizard.xml',
        'views/sale_order_views.xml'
    ],
    'installable': True,
    'application': True,
    'auto_install': False,   
}