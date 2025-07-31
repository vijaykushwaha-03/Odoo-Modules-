{
    'name': 'Wise Project',
    'version': '1.0',   
    'description': """This is a simple example module for wisenetic project overrite.""",
    "license":"LGPL-3",
    'depends': ['base'],
    'data': [        
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/project.xml',
        'views/task.xml'
    ],
    'installable': True,
    'application': True,
    'auto_install': False,   
}
