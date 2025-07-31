from odoo import models, fields

class WiseProject(models.Model):
    _name = 'wise.project'
    _description = 'Wisenetic Project'

    name = fields.Char(string='Project Name', required=True)
    progress = fields.Integer(string='Progress')
    status = fields.Selection([('todo', 'To do'), ('in_process', 'In Process'), ('completed', 'Completed')], string='Status')
    last_update_task = fields.Char(string='last_update_task')

    #tasks_ids = fields.One2many('wise.task', 'project_id', string="Tasks")
    