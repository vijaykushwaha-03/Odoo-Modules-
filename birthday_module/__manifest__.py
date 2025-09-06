{
    "name":"Birthday-Wishes",
    "author":"Odoo custom",
    "license":"LGPL-3", 
    "version":"1.0",
    'depends': ['mail'],
    "data":[      
        "security/ir.model.access.csv",
        "data/ir_cron.xml",
        "data/birthday_email_template.xml",
        "views/users_detail.xml",
       
    ]
}