# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class PortalLeave(http.Controller):
    @http.route('/leave', auth='public', website=True)
    def index(self, **kw):
        # return "Hello, world"
        a = "hallooo"
        all_leaves = request.env['hr.leave'].sudo().search([])
        print(all_leaves)
        return request.render('portal_leave.leave_request_portal',
                              {'all_leaves': all_leaves})
