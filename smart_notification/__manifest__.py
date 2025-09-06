{
    'name': 'Smart Notification',
    'version': '1.0', 
    'license': 'LGPL-3',  
    'description': """This is a simple example module for Smart Notification.""",
    'depends': ['base','sale'],
    'uninstall_hook': 'uninstall_hook',
    'data': [        
        'security/ir.model.access.csv',
        'views/notification_menu.xml',
        'views/sale_order_views.xml'
        
    ],
    'installable': True,
    'application': True,
    'auto_install': False,   
}