# -*- coding: utf-8 -*-

from odoo import http, fields
from odoo.http import request
from odoo.addons.website_sale.controllers.main import QueryURL


class PortalLeave(http.Controller):
    @http.route('/leave', auth='public', website=True)
    def index(self, **kw):
        """ Showing All the leaves created """

        all_leaves = request.env['hr.leave'].sudo().search(
            [('user_id', '=', request.env.uid)])
        print(all_leaves)
        keep = QueryURL()
        print("LLL", keep)
        values = {}
        return request.render('portal_leave.leave_request_portal',
                              {'all_leaves': all_leaves, 'keep': keep})

    @http.route('/leave/delete', auth='public', type='http', website=True,
                csrf=False)
    def _onclick_delete(self, id=None, **kw):
        """ Cancel button Click """
        if id:
            print(id)
            request.env['hr.leave'].sudo().search(
                [('id', '=', id)]).unlink()
        vals = "Record Deleted"
        return request.render('portal_leave.leave_request_form_success',
                              {'vals': vals})


""" Leave Request Creation Form Class"""


class RequestLeave(http.Controller):
    @http.route('/leave/request', auth='public', website=True)
    def index(self, **kw):
        """ Leave request Creation Form"""
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
        """ Submit Button Press. Create a leave """
        curent = fields.Many2one('hr.employee', "current_user",
                                 default=lambda self: self.env.user)
        print(curent)
        current_user = request.env['hr.employee'].sudo().search(
            [('user_id', '=', request.env.uid)])
        print(current_user.name)
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
            duration = 0
            end_date = post.get('start_date')
        else:
            end_date = post.get('end_date')
        if post.get('#custom_hours'):
            print("hai", post.get('#leave_type_to'))
            print(post.get('#leave_type_from'))
            duration = 0
            end_date = post.get('start_date')
        else:
            duration = post.get('#duration')
        print(end_date)
        print(post.get('start_date'))
        if not end_date:
            end_date = post.get('start_date')
        if (post.get('start_date') and end_date and post.get(
                'start_date') <= end_date) or post.get('#custom_hours'):
            leave_request = request.env['hr.leave'].sudo().create({
                'holiday_status_id': leave_id.id,
                'request_date_from': post.get('start_date'),
                'request_date_to': post.get('start_date'),
                'number_of_days': duration,
                'name': post.get('description'),
                'request_date_from_period': post.get('#time_period'),
                'request_unit_hours': post.get('custom_hours'),
                'request_unit_half': post.get('half_day'),
                'request_hour_from': post.get('#leave_type_from'),
                'request_hour_to': post.get('#leave_type_to'),
                'employee_id': current_user.id,
                'holiday_type': "employee",
                'department_id': current_user.department_id.id,
            })
            print(leave_request)
            # vals = {'leave_request': leave_request, }
            # print(vals)
            vals = " Leave Created"
            return request.render('portal_leave.leave_request_form_success',
                                  {'vals': vals,
                                   'leave_request': leave_request})
        else:
            alert_date = "Start Date must be lesser than End date"
            return request.render('portal_leave.request_leave_apply',
                                  {'alert_date': alert_date,
                                   'leave_type': leave_type})
