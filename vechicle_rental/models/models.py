# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.tools.safe_eval import datetime


class VehicleRental(models.Model):
    _name = 'vehicle.rental'
    _description = " Vehicle rental app"

    print("HAi NEXT CHECK")
    vehicle = fields.Many2one('fleet.vehicle', string='Vehicle')
    name = fields.Char(string='Name', required=True)
    brand = fields.Char(string='Brand')
    registration_date = fields.Date('Registration Date ', required=False,
                                    help='Date when the vehicle has been Register')
    model = fields.Char(string='model')
    rent = fields.Float(string="Rent", digits=(6, 2))

    # @api.onchange('model_id')
    # def on_change_model_id(self):
    #      brand = self.brand_id
