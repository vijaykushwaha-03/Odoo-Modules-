{
    'name': 'Demo Data Electronic Store',
    'version': '1.0',   
    'description': """This is a simple example module for wisenetic project overrite.""",
    "license":"LGPL-3",
    'depends': ['product','website_sale'],
    'data': [
        'data/product_category_demo.xml',
        'data/product_attribute_demo.xml'
    ],
    'demo':[
        'data/product_demo.xml',
        'data/demo.xml',
    ],
    
    'installable': True,
    'application': True,
    'auto_install': False,   
}
