from odoo import models,fields,api

class Users(models.Model):
    _inherit = "res.partner"

    birthday = fields.Date()  
    
   