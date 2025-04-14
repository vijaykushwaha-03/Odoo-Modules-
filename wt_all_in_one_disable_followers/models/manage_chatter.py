from odoo import models, fields

class ManageChatter(models.Model):
    _name = 'manage.chatter'
    _description = 'Manage Chatter'

    name = fields.Char(string='Name', required=True)
    active = fields.Boolean(string='Active')
    model_ids = fields.Many2many('ir.model', string='Models')
    disable_to_add_followers = fields.Many2many('ir.model.fields.selection', domain="[('field_id.model_id', 'in', model_ids), ('field_id.name', '=', 'state')]", string='Disable to add Followers')
    users = fields.Many2many('res.users', string='Users')

    def get_restricted_models_states(self, model_name, current_user):
        """Return a list of restricted states for the given model and user."""
        chatter = self.search([
            ('model_ids.model', '=', model_name),
            ('active', '=', True),  # Ensure the chatter rule is active
            ('users', 'in', [current_user.id])  # Check if the user is restricted
        ], limit=1)

        return chatter.disable_to_add_followers.mapped('value') if chatter else []