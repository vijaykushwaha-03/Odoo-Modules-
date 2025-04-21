import base64
import logging
import io
from odoo import http
from odoo.http import request
from werkzeug.wrappers import Response
from odoo.addons.web.controllers.binary import Binary
from odoo.tools.mimetypes import guess_mimetype
try:
    from werkzeug.utils import send_file
except ImportError:
    from odoo.tools._vendor.send_file import send_file

_logger = logging.getLogger(__name__)

class Main(http.Controller):

    @http.route('/web/binary/pos_logo', type='http', auth="user", cors="*")
    def pos_logo(self):
        try:
            config = request.env['pos.config'].sudo().search([], limit=1)

            if(config.enable_pos_logo):
                if config.logo_option == 'custom':
                    image_base64 = base64.b64decode(config.custom_logo)
                    image_data = io.BytesIO(image_base64)

                    mimetype = guess_mimetype(image_base64, default='image/png')
                    imgext = '.' + mimetype.split('/')[1]
                    if imgext == '.svg+xml':
                        imgext = '.svg'

                    return send_file(
                        image_data,
                        request.httprequest.environ,
                        download_name='pos_logo' + imgext,
                        mimetype=mimetype,
                        response_class=Response,
                    )
                else:
                    if config.logo_option == 'company':
                        return Binary().company_logo()

        except Exception as e:
            _logger.error('Error fetching POS logo: %s', e)
            return http.Response(status=500)
