# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.tools.safe_eval import datetime


class VehicleRental(models.Model):
    _name = 'vehicle.rental'
    _description = " Vehicle rental app"
    _inherit =

    print("HAi NEXT CHECK")
    vehicle = fields.Selection([('fleet.vehicle','car')],'vehicle')
    name = fields.Char(string='Name', required=True)
    brand = fields.Char(string='Brand')
    registration_date = fields.Date('Registration Date ', required=False,
                                    help='Date when the vehicle has been Register')
    model = fields.Char(string='model')
    rent = fields.Float(string="Rent", digits=(6, 2))
