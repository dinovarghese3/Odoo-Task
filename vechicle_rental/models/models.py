# -*- coding: utf-8 -*-
from odoo import models, fields, api


class VehicleRental(models.Model):
    _name = 'vehicle.rental'
    _description = " Vehicle rental app"

    vehicle_id = fields.Many2one('fleet.vehicle', string='Vehicle',
                                 domain=[('state_id', '=', 3)])
    name = fields.Char(string='Name', required=True)
    brand = fields.Char(string='Brand')
    registration_date = fields.Date('Registration Date ', required=False,
                                    help='Date the vehicle has Register')
    model = fields.Char(string='Model')
    currency_id = fields.Many2one('res.currency', string='Currency',
                                  default=lambda self: self.env.user.company_id.id)
    rent = fields.Monetary(string='Rent')
    state = fields.Selection(
        [('available', 'Available'), ('notavailable', 'Not available'),
         ('sold', 'Sold')],
        string='State', default='available')

    # def on_change_model_id(self):
    #      brand = self.brand_id
    @api.onchange('vehicle_id')
    def onchange_vehicle(self):
        for rec in self:
            if rec.vehicle_id:
                rec.registration_date = rec.vehicle_id.registration_date
                # rec.brand='fleet.vehicle.model'.rec.vehicle_id.brand_id
                print(rec.vehicle_id)


class RegisterDate(models.Model):
    _inherit = 'fleet.vehicle'

    registration_date = fields.Date('Registration Date ', required=False,
                                    help='Date when the vehicle has been '
                                         'Register')
