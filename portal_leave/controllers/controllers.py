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

    @http.route('/leave/delete', auth='public', website=True)
    def _onclick_delete(self, **kw):
        print(self)
        request.env['hr.leave'].sudo().search([()]).unlink()
        # return request.render("Hi")
        # return super(hr_leave, self).unlink()


class RequestLeave(http.Controller):
    @http.route('/leave/request', auth='public', website=True)
    def index(self, **kw):
        leave_type = request.env['hr.leave.type'].sudo().search([])
        # custom_hour=request.env['hr.leave'].sudo().search([])
        request_hour_from = [
            ('0', '12:00 AM'), ('0.5', '12:30 AM'),
            ('1', '1:00 AM'), ('1.5', '1:30 AM'),
            ('2', '2:00 AM'), ('2.5', '2:30 AM'),
            ('3', '3:00 AM'), ('3.5', '3:30 AM'),
            ('4', '4:00 AM'), ('4.5', '4:30 AM'),
            ('5', '5:00 AM'), ('5.5', '5:30 AM'),
            ('6', '6:00 AM'), ('6.5', '6:30 AM'),
            ('7', '7:00 AM'), ('7.5', '7:30 AM'),
            ('8', '8:00 AM'), ('8.5', '8:30 AM'),
            ('9', '9:00 AM'), ('9.5', '9:30 AM'),
            ('10', '10:00 AM'), ('10.5', '10:30 AM'),
            ('11', '11:00 AM'), ('11.5', '11:30 AM'),
            ('12', '12:00 PM'), ('12.5', '12:30 PM'),
            ('13', '1:00 PM'), ('13.5', '1:30 PM'),
            ('14', '2:00 PM'), ('14.5', '2:30 PM'),
            ('15', '3:00 PM'), ('15.5', '3:30 PM'),
            ('16', '4:00 PM'), ('16.5', '4:30 PM'),
            ('17', '5:00 PM'), ('17.5', '5:30 PM'),
            ('18', '6:00 PM'), ('18.5', '6:30 PM'),
            ('19', '7:00 PM'), ('19.5', '7:30 PM'),
            ('20', '8:00 PM'), ('20.5', '8:30 PM'),
            ('21', '9:00 PM'), ('21.5', '9:30 PM'),
            ('22', '10:00 PM'), ('22.5', '10:30 PM'),
            ('23', '11:00 PM'), ('23.5', '11:30 PM')]

        # custom_hour_typ=custom_hour.request_hour_from
        leave = request.env['hr.leave'].name
        print(leave)
        # selection=leave.request_hour_from
        # print(selection)
        return request.render('portal_leave.request_leave_apply',
                              {'leave_type': leave_type,
                               'request_hour_from': request_hour_from,
                               })

    @http.route('/leave/request/submit', type='http', auth='public',
                website=True, csrf=False)
    def leave_request_submition(self, **post):
        current_user = request.env['res.users'].sudo().search(
            [('id', '=', http.request.env.context.get('uid'))])
        leave_type = request.env['hr.leave.type'].sudo().search([])
        print(current_user.name)
        print(current_user)
        print(post)
        alert_date = ""
        # leave_type = post.get('leave_type')
        # print(leave_type)
        leave_id = request.env['hr.leave.type'].sudo().search(
            [('name', '=', post.get('leave_type'))])
        print(leave_id.id)
        if post.get('half_day'):
            end_date = post.get('start_date')
        else:
            end_date=post.get('end_date')
        if post.get('start_date') and post.get('start_date') and post.get(
                'start_date') < post.get(
            'end_date'):
            leave_request = request.env['hr.leave'].create({
                'holiday_status_id': leave_id.id,
                'request_date_from': post.get('start_date'),
                'request_date_to': end_date,
                'name': post.get('description'),
                'request_unit_half':post.get('half_day'),
                'employee_id': current_user.id,
                'holiday_type': "employee"

            })
            print(leave_request)
            vals = {'leave_request': leave_request, }
            print(vals)
            return request.render('portal_leave.leave_request_form_success',
                                  vals)
        else:
            alert_date = "Start Date must be lesser than End date"
            return request.render('portal_leave.request_leave_apply',
                                  {'alert_date': alert_date,
                                   'leave_type': leave_type})
