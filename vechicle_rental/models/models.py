# -*- coding: utf-8 -*-
from odoo import models, fields, api


class VehicleRental(models.Model):
    _name = 'vehicle.rental'
    _description = " Vehicle rental app"

    vehicle_id = fields.Many2one('fleet.vehicle', string='Vehicle',
                                 domain=[('state_id', '=', 3)])
    name = fields.Char(string='Name', required=True)
    brand_id = fields.Many2one(string='Brand',
                               related='vehicle_id.brand_id', store=True)
    print(brand_id)
    registration_date = fields.Date('Registration Date ', required=False,
                                    help='Date the vehicle has Register',
                                    readonly=True,
                                    related='vehicle_id.registration_date')
    model = fields.Char(string='Model')
    currency_id = fields.Many2one('res.currency', string='Currency',
                                  default=lambda
                                      self: self.env.user.company_id.id)
    rent = fields.Monetary(string='Rent')
    state = fields.Selection(
        [('available', 'Available'), ('notavailable', 'Not available'),
         ('sold', 'Sold')],
        string='State', default='available')


class RegisterDate(models.Model):
    _inherit = 'fleet.vehicle'

    registration_date = fields.Date('Registration Date ', required=False,
                                    help='Date when the vehicle has been '
                                         'Register')
