import logging
import werkzeug
from werkzeug.urls import url_encode

from odoo import http, tools, _
from odoo.addons.auth_signup.models.res_users import SignupError
from odoo.addons.web.controllers.home import ensure_db, Home, SIGN_UP_REQUEST_PARAMS, LOGIN_SUCCESSFUL_PARAMS
from odoo.addons.base_setup.controllers.main import BaseSetup
from odoo.exceptions import UserError
from odoo.http import request
from markupsafe import Markup

_logger = logging.getLogger(__name__)

LOGIN_SUCCESSFUL_PARAMS.add('account_created')


# class AuthSignupHome(Home):

#     @http.route('/web/signup', type='http', auth='public', website=True, sitemap=False)
#     def web_auth_signup(self, *args, **kw):
#         pass
#         res = super().web_login(redirect=redirect, **kw)

#         uid = request.session.uid
#         if uid:
#             user = request.env['res.users'].sudo().browse(uid)
#             _logger.info(f"✅ User logged in: {user.name} ({user.login})")
        