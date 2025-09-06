from . import models

def uninstall_hook(env):
    alert_views = env['ir.ui.view'].search([('name', 'ilike', '.alert.')])
    alert_views.unlink()
