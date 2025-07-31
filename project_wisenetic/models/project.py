from odoo import models, fields, api

class Project(models.Model):
    _name = 'wisenetic.project'
    
    name = fields.Char(string='Name', required=True)
    status = fields.Selection(
        selection=[
            ('to_do', "To Do"),
            ('in_progress', "In Progress"),
            ('completed', "Completed"),
        ],
        string= 'Status',
        default = 'to_do'
    )      
    task_ids = fields.One2many('wisenetic.task', 'project_id', string='Tasks')
    progress = fields.Char(string="Progress" ,compute='calculate_percentage')
    
    last_update = fields.Char(string='last_update_task')

    # is_active = fields.Boolean(string="Is_Active", default=True)

    # last_update = fields.Char(string='last_update_task', compute="last_update_task" )
    
    # def last_update_task(self):
    #     for record in self:
    #         if record.name:
    #             last_task = record.task_ids.sorted('write_date', reverse=True)[:1]
    #             record.last_update = last_task.name if last_task else ""
    
    @api.depends('task_ids','progress')
    def calculate_percentage(self):
        for record in self:
            total_task = len(record.task_ids)

            if total_task > 0:
                total_task_progress = 0 

                for task in record.task_ids:
                    total_task_progress += task.progress                                    
                total_progress = total_task_progress / total_task

                if total_progress == 0 or total_progress == 100:
                    record.progress = f'{round(total_progress)}%'
                else:
                    record.progress = f'{round(total_progress, 2)}%'

                if total_progress == 100:
                    record.status = "completed"
                elif total_progress == 0:
                    record.status = "to_do"
                else:
                    record.status = "in_progress"                                
            else:
                record.progress = "0%"
   

   