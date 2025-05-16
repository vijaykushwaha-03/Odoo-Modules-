import ast
from odoo import models, fields,api
from odoo.exceptions import UserError

class SmartNotificationRule(models.Model):
    _name = 'smart.notification.rule'
    _description = 'Notifications menu'

    name = fields.Char(string="Name")
    message = fields.Text(string="Message", help=" placeholder {field_name} to insert record fields dynamically.")
    model_id = fields.Many2one("ir.model", string="Model")
    user_ids =fields.Many2many("res.users", string="User")
    group_id = fields.Many2one("res.groups",string="Group")
    type = fields.Selection([
        ('alert-primary', 'Alert Primary'),
        ('alert-secondary', 'Alert Secondary'),
        ('alert-success', 'Alert Success'),
        ('alert-danger', 'Alert Danger'),
        ('alert-warning', 'Alert Warning'),
        ('alert-info', 'Alert Info')],)
    company_id = fields.Many2one("res.company", string="Company", default=lambda self: self.env.company)
    domain = fields.Char(string="Domain")
    record_count = fields.Integer(string="Total Record Preview",compute='_compute_record_count')
    active = fields.Boolean(string="Active",default=False)
    state = fields.Selection(
        [('draft', 'Draft'), ('done', 'Done'), ('cancelled', 'Cancelled')],
        string='State', help='Different Stages', default="draft")
    view_id = fields.Many2one('ir.ui.view', string='View',
                              help='Select the view for smart alerts',
                              domain='[("model", "=", model_name), '
                                     '("type", "=", "form")]')

    new_view_id = fields.Many2one('ir.ui.view',
                                  string="Created New view Id",
                                  help='It will automatically create a view'
                                       ' record while saving the form',
                                  readonly=True)
    model_name = fields.Char(related="model_id.model",
                             string='Model Name', help='Model Name')

    
    def action_apply(self):
            model = self.model_id
            model_view = self.view_id
            class_name = 'alert ' + self.type
            xml_id = ''
            if self.group_id.id:
                xml_ids = self.group_id.get_external_id()
                xml_id = xml_ids.get(self.group_id.id)
            filter = ast.literal_eval(self.domain)     
            for i in range(len(filter)):
                if filter[i] == '&':
                    filter[i] = '|'
                elif filter[i] == '|':
                    filter[i] = '&amp;'
                else:
                    if filter[i][1] == '=':
                        filter_list = list(filter[i])
                        filter_list[1] = '!='
                        filter = f" {filter_list[0]} {filter_list[1]} '{filter_list[2]}'"
                    elif filter[i][1] == '!=':
                        filter_list = list(filter[i])
                        filter_list[1] = '=='
                        filter = f" {filter_list[0]} {filter_list[1]} '{filter_list[2]}'"
                    elif filter[i][1] == '>':
                        filter_list = list(filter[i])
                        filter_list[1] = '&lt;'
                        filter = f" {filter_list[0]} {filter_list[1]} {filter_list[2]}"
                    elif filter[i][1] == '<':
                        filter_list = list(filter[i])
                        filter_list[1] = '&gt;'
                        filter = f" {filter_list[0]} {filter_list[1]} {filter_list[2]}"
                    elif filter[i][1] == '>=':
                        filter_list = list(filter[i])
                        filter_list[1] = '&lt;='
                        filter = f" {filter_list[0]} {filter_list[1]} {filter_list[2]}"
                    elif filter[i][1] == '<=':
                        filter_list = list(filter[i])
                        filter_list[1] = '&gt;='
                        filter = f" {filter_list[0]} {filter_list[1]} {filter_list[2]}"
                    elif filter[i][1] == 'ilike':
                        filter_list = list(filter[i])
                        filter_list[1] = 'not in'
                        filter = f" {filter_list[0]} {filter_list[1]} ['{filter_list[2]}']"
                    elif filter[i][1] == 'not ilike':
                        filter_list = list(filter[i])
                        filter_list[1] = 'in'
                        filter = f" {filter_list[0]} {filter_list[1]} ['{filter_list[2]}']"
                    elif filter[i][1] == 'in':
                        filter_list = list(filter[i])
                        filter_list[1] = 'not in'
                        filter = f" {filter_list[0]} {filter_list[1]} {filter_list[2]}"
                    elif filter[i][1] == 'not in':
                        filter_list = list(filter[i])
                        filter_list[1] = 'in'
                        filter = f" {filter_list[0]} {filter_list[1]} {filter_list[2]}"

            invisible_filter = str(filter).replace("'", '"')
            if xml_id:
                if invisible_filter != '[]':
                    arch = '<xpath expr="//sheet" position="before">' + '<div role="alert" class="' + class_name + '" ' + ' groups="' + xml_id + '"' + """ invisible=' """ + invisible_filter + "'" + '>' + self.message + '</div></xpath>'
                else:
                    arch = '<xpath expr="//sheet" position="before">' + '<div role="alert" class="' + class_name + '" ' + ' groups="' + xml_id + '"' + '>' + self.message + '</div></xpath>'
            else:
                if invisible_filter != '[]':
                    arch = '<xpath expr="//sheet" position="before">' + '<div role="alert" class="' + class_name + '" ' + """ invisible='""" + invisible_filter + "'" + '>' + self.message + '</div></xpath>'
                else:
                    arch = '<xpath expr="//sheet" position="before">' + '<div role="alert" class="' + class_name + '" ' + '>' + self.message + '</div></xpath>'

            if model_view:
                view_data = {
                    'name': self.type + '.alert.' + model_view.name + '.' + str(
                        self.id),
                    'type': 'form',
                    'model': model.model,
                    'priority': 1,
                    'inherit_id': model_view.id,
                    'mode': 'extension',
                    'arch_base': arch.encode('utf-8')
                }
                try:
                    view = self.env["ir.ui.view"].create(view_data)
                except:
                    raise UserError("Can't create a view based on this domain")
                self.new_view_id = view
                self.state = 'done'

    def action_cancel(self):
            self.state = 'cancelled'
            self.new_view_id.unlink()

    def reset_draft(self):
            self.state = 'draft'

    def unlink(self):
        for rec in self:
            if rec.new_view_id:
                rec.new_view_id.unlink()
        return super(SmartNotificationRule, self).unlink()
    

    



