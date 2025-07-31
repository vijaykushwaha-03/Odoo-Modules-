from odoo import models, fields, api, exceptions

class Task(models.Model):
    _name = 'wisenetic.task'
    
    name = fields.Char(string='Name', required=True)
    progress = fields.Integer(string='progress', default=0)
    status = fields.Selection(
        [
            ("to_do","To Do"),
            ("in_process","In Process"),
            ("completed","Completed")
        ],
        default="to_do",
    )

    project_id = fields.Many2one('wisenetic.project', string="Project")
    #project_id = fields.Many2one('wisenetic.project', string='Project')
 

    @api.onchange('progress')
    def _onchange_progress(self):
        if self.progress == 100:
            self.status = "completed" 
        elif self.progress == 0:
            self.status = "to_do"
        elif self.progress > 0 and self.progress < 100:
            self.status = "in_process"

    @api.onchange('status')
    def _onchange_status(self):
        if self.status == 'to_do':
            self.progress = 0
        elif self.status == 'completed':
            self.progress = 100

            # RANGE VALIDATION
    @api.constrains('progress')
    def progress_range(self):
        if self.progress < 0 or self.progress > 100:
            raise exceptions.ValidationError("Enter Value Between 0 to 100")
        
            # OVERRIDE   
            
    @api.model
    def create(self, vals):        
        if "name" in vals:
            vals["name"] = "hello " + vals["name"]
        return super(Task, self).create(vals)
    

    def write(self, values):
        res = super(Task, self).write(values)
        print(values)
        self.project_id.write({"last_update": self.name})
        return res

 