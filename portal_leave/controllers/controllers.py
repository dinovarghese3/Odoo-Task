# -*- coding: utf-8 -*-
""" Leave request creation from website  """
from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import QueryURL


class PortalLeave(http.Controller):
    """Showing All leave request created"""

    @http.route('/leave', auth='public', website=True)
    def index(self):
        """ Showing All the leaves created """

        all_leaves = request.env['hr.leave'].sudo().search(
            [('user_id', '=', request.env.uid)])
        keep = QueryURL()  # For sending value in url
        return request.render('portal_leave.leave_request_portal',
                              {'all_leaves': all_leaves, 'keep': keep})

    @http.route('/leave/delete', auth='public', type='http', website=True,
                csrf=False)
    def _onclick_delete(self, id=None):
        """ Cancel button Click """
        if id:
            # id of leave request from Url
            request.env['hr.leave'].sudo().search(
                [('id', '=', id)]).unlink()
        vals = "Record Deleted"
        return request.render('portal_leave.leave_request_form_success',
                              {'vals': vals})


class RequestLeave(http.Controller):
    """ Leave Request Creation Form Class"""
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
    index_of_to = 0.0
    index_of_from = 0.0

    @http.route('/leave/request', auth='public', website=True)
    def index(self, **kw):
        """ Leave request Creation Form"""
        leave_type = request.env['hr.leave.type'].sudo().search([])
        return request.render('portal_leave.request_leave_apply',
                              {'leave_type': leave_type,
                               'request_hour_from': self.request_hour_from,
                               })

    @http.route('/leave/request/submit', type='http', auth='public',
                website=True, csrf=False)
    def leave_request_submition(self, **post):
        """ Submit Button Press. Create a leave """
        current_user = request.env['hr.employee'].sudo().search(
            [('user_id', '=',
              request.env.uid)])  # getting current user loged in
        leave_type = request.env['hr.leave.type'].sudo().search([])
        alert_date = ""
        duration = 0
        leave_id = request.env['hr.leave.type'].sudo().search(
            [('name', '=', post.get(
                'leave_type'))])  # geting the leave type the user selected
        if post.get('half_day'):
            # checking the Half day check box is enabled or not if enabled set
            # the duration as 4 and set the start date and end date same
            duration = 4
            end_date = post.get('start_date')
        else:
            end_date = post.get('end_date')
        if post.get('custom_hours'):
            # checking the custom hours in checked or not
            duration = 0
            for i in self.request_hour_from:
                if i[1] == post.get('leave_type_to'):
                    self.index_of_to = i[0]
                    print("to", self.index_of_to)
                if i[1] == post.get('leave_type_from'):
                    self.index_of_from = i[0]
                    print("from", self.index_of_from)
            duration = float(self.index_of_from) - float(self.index_of_to)
            print("duration custom_hour", duration, self.index_of_from,
                  self.index_of_to)
            end_date = post.get(
                'start_date')  # seting the end date same as start date
        else:
            duration = post.get('duration')

        if not self.index_of_from and not self.index_of_to:
            self.index_of_from = 0.0
            self.index_of_to = 0.0
        if (post.get('start_date') and end_date and post.get(
                'start_date') <= end_date) or post.get('custom_hours'):
            leave_request = request.env['hr.leave'].sudo().create({
                'holiday_status_id': leave_id.id,
                'request_date_from': post.get('start_date'),
                'request_date_to': end_date,
                'number_of_days': duration,
                'name': post.get('description'),
                'request_date_from_period': post.get('time_period'),
                'request_unit_hours': post.get('custom_hours'),
                'request_unit_half': post.get('half_day'),
                'request_hour_from': self.index_of_from,
                'request_hour_to': self.index_of_to,
                'employee_id': current_user.id,
                'holiday_type': "employee",
                'department_id': current_user.department_id.id,
            })
            vals = " Leave Created"
            return request.render('portal_leave.leave_request_form_success',
                                  {'vals': vals,
                                   'leave_request': leave_request})
        else:
            alert_date = "Start Date must be lesser than End date"
            return request.render('portal_leave.request_leave_apply',
                                  {'alert_date': alert_date,
                                   'leave_type': leave_type})
