from odoo import fields, models, _, api
from odoo.exceptions import UserError


class VehicleRentReport(models.TransientModel):
    _name = "vehicle.report"
