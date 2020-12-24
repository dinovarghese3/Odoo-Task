# -*- coding: utf-8 -*-
from odoo.addons import fleet
from odoo import models, fields, api


class VehicleRental(models.Model):
    _name = 'vehicle.rental'
    _description = " Vehicle rental app"

    print("HAi NEXT CHECK")
    vehicle = fields.Many2one('fleet.vehicle','vehicle')
    vehicle_type = fields.Char(string='vehicle Type')
    name = fields.Char(string='Name', required=True)
