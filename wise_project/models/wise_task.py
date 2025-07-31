from odoo import models, fields, api

class WiseTask(models.Model):
    _name = 'wise.task'
    _description = 'Wisenetic Task'

    name = fields.Char(string='Name', required=True)
    project = fields.Many2one('wise.project', string='Project') 
    progress = fields.Integer(string='Progress')
    status = fields.Selection([('todo', 'To do'), ('in_process', 'In Process'), ('completed', 'Completed')], string='Status',
                                compute='_compute_progress_status', inverse='_compute_status_progress')

    #project_id = fields.Many2one('wise.project', string="Project")

    @api.depends('progress')
    def _compute_progress_status(self):
        for percentage in self:
            if percentage.progress == 0:
                percentage.status = 'todo'
            elif 1 <= percentage.progress <= 99:
                percentage.status = 'in_process'
            elif percentage.progress == 100:
                percentage.status = 'completed'

    @api.onchange('status')
    def _compute_status_progress(self):
        for task in self:
            if task.status == 'todo':
                task.progress = 0
            elif task.status == 'completed':
                task.progress = 100
