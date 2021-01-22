from odoo import fields, models, _, api
from odoo.exceptions import UserError


class VehicleRentReport(models.TransientModel):
    _name = 'vehicle.report'

    vehicle_id = fields.Many2many('vehicle.rental')
    from_date = fields.Date('From Date')
    to_date = fields.Date('To Date')

    def view_report_pdf(self):
        print(self)
        data = {
            'model_id': self.id,
            'from_date': self.from_date,
            'to_date': self.to_date,
            'vehicle_id': self.vehicle_id.name,
            've_id':self.vehicle_id.id,
        }
        print(self.id)
        # used_context = self._build_contexts(data)
        # data['form']['used_context'] = dict(used_context)
        return self.env.ref(
            'vechicle_rental.print_report_pdf').report_action(self,
                                                              data=data)
