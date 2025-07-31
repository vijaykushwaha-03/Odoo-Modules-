from odoo import api, fields, models


class StudentInfo(models.Model):
    _name = "student.info"
    _descriptionn = "Student Details" 
 
    name = fields.Char(string='Name', required=True)
    description = fields.Char(string='Description')
    date_of_birth = fields.Date(string='DOB')
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string='Gender')