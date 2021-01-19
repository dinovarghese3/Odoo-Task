from odoo import models


class ReportVehicleRent(models.AbstractModel):
    _name = 'report.vehicle.rent'
    def _get_rent_report(self):
        print("Hallo")
        cr = self.env.cr
        move_line = self.env['vehicle.report']
        move_lines = {x: [] for x in accounts.ids}

