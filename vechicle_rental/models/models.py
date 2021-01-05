# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.tools.safe_eval import datetime


class VehicleRental(models.Model):
    _name = 'vehicle.rental'
    _description = "Class contain all Vehicle details"

    vehicle_id = fields.Many2one('fleet.vehicle', string='Vehicle',
                                 domain=[('state_id', '=', 3)])
    name = fields.Char(string='Name', compute='_compute_name',
                       related='vehicle_id.name',
                       store=True)
    brand_id = fields.Many2one(string='Brand',
                               related='vehicle_id.brand_id', store=True)
    registration_date = fields.Date('Registration Date ', required=False,
                                    help='Date the vehicle has Register',
                                    readonly=True,
                                    related='vehicle_id.registration_date')
    model = fields.Char(string='Model')
    currency_id = fields.Many2one('res.currency', string='Currency',
                                  default=lambda
                                      self: self.env.user.company_id.currency_id)

    rent = fields.Monetary(string='Rent')
    state = fields.Selection(
        [('available', 'Available'), ('notavailable', 'Not available'),
         ('sold', 'Sold')],
        string='State', default='available')
    all_request_ids = fields.One2many('vehicle.request', 'vehicle_id',
                                  string='All Requests', store=True)
    rent_charges_ids = fields.One2many('rent.charges', 'vehicle_id')

    def all_rental_requests(self):
        """ Function for Smart button to return the car requests"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Requests',
            'view_mode': 'tree,form',
            'res_model': 'vehicle.request',
            'domain': [('vehicle_id', '=', self.name)],
            'context': "{'create': False}"
        }

    @api.onchange('registration_date')
    def _onchange_registration_date(self):
        """ Calculating Year from registration date """
        # print('contry', self.env.user.company_id.id)
        # print(self.registration_date)
        if self.registration_date:
            self.model = str((datetime.datetime.strptime(
                str(self.registration_date), "%Y-%m-%d")).year)


class RentCharges(models.Model):
    """Amount calculation based on date"""
    _name = 'rent.charges'
    vehicle_id = fields.Many2one('vehicle.rental', string="vehicle")
    currency_id = fields.Many2one('res.currency', string='Currency',
                                  default=lambda
                                      self: self.env.user.company_id.currency_id)
    amount = fields.Monetary(string='Amount')
    time = fields.Selection([('hour', 'Hour'), ('day', 'Day'), ('week', 'Week'),
                             ('month', 'Month')], string="Time", default='day')


class RegisterDate(models.Model):
    """ Adding new field registration date to fleet module """
    _inherit = 'fleet.vehicle'

    registration_date = fields.Date('Registration Date ', required=False,
                                    help='Date when the vehicle has been '
                                         'Register')
