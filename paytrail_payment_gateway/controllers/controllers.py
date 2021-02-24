import logging
import pprint
import werkzeug
from werkzeug.utils import redirect
from odoo import http
from odoo.http import request
_logger = logging.getLogger(__name__)


class AtomController(http.Controller):
    @http.route(['/payment/paytrail/return/', '/payment/paytrail/cancel/', '/payment/paytrail/error/'],
                type='http', auth='public', csrf=False)
    def paytm_return(self, **post):


        _logger.info(
            'Paytrail: entering form_feedback with post data %s', pprint.pformat(post))
        if post:
            request.env['payment.transaction'].sudo().form_feedback(post, 'paytrail')
        return werkzeug.utils.redirect('/payment/process')