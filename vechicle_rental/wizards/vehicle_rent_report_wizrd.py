from odoo import fields, models, _, api
from odoo.exceptions import UserError


class VehicleRentReport(models.TransientModel):
    _name = 'vehicle.report'

    vehicle_id = fields.Many2one('vehicle.request')
    from_date = fields.Date('From Date')
    to_date = fields.Date('To Date')
