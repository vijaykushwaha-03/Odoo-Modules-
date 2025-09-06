{
    "name": "Password Expiration",
    "summary": "Allow admin to set password security requirements.",
    'author': "Odoo custom",
    'website': "https://www.Odoo custom.com",
    "support": "info@Odoo custom.com",
    'version': '18.0.0.0.1',
    "category": "Base",
    "depends": ["auth_signup", "auth_password_policy_signup", "auth_password_policy","website"],
    "license": "LGPL-3",
    "data": [
        "security/ir.model.access.csv",
        "views/res_config_settings_views.xml",
        "data/password_expire_notification_templates.xml",
        "data/cron_send_mail.xml", 
    ], 

    'installable': True,
    'application': True,
    'auto_install': False,
}
