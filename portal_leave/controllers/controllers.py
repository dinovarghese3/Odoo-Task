# -*- coding: utf-8 -*-
from odoo import http, fields
from odoo.http import request


class PortalLeave(http.Controller):
    @http.route('/leave', auth='public', website=True)
    def index(self, **kw):
        all_leaves = request.env['hr.leave'].sudo().search([])
        print(all_leaves)
        return request.render('portal_leave.leave_request_portal',
                              {'all_leaves': all_leaves})


class RequestLeave(http.Controller):
    @http.route('/leave/request', auth='public', website=True)
    def index(self, **kw):
        leave_type = request.env['hr.leave.type'].sudo().search([])
        return request.render('portal_leave.request_leave_apply',
                              {'leave_type': leave_type})

    @http.route('/leave/request/submit', type='http', auth='public',
                website=True, csrf=False)
    def leave_request_submition(self, **post):
        current_user = request.env['res.users'].sudo().search(
            [('id', '=', http.request.env.context.get('uid'))])
        print(current_user.name)
        print(current_user)
        print(post)
        # leave_type = post.get('leave_type')
        # print(leave_type)
        leave_id = request.env['hr.leave.type'].sudo().search(
            [('name', '=', post.get('leave_type'))])
        print(leave_id.id)

        leave_request = request.env['hr.leave'].create({
            'holiday_status_id': leave_id.id,
            'request_date_from': post.get('start_date'),
            'request_date_to': post.get('end_date'),
            'name': post.get('description'),
            'employee_id': current_user.id,
            'holiday_type': "employee"

        })
        print(leave_request)
        vals = {'leave_request': leave_request, }
        print(vals)
        return request.render('portal_leave.leave_request_form_success',
                              vals)
