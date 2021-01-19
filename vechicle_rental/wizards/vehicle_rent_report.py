from odoo import fields, models, _
from odoo.exceptions import UserError


class VehicleRentReport(models.TransientModel):
    _name = "vehicle.report"
    sequence_id = fields.Many2one('vehicle.request')
    vehicle_id = fields.Many2one('vehicle.rental', )
    customer_id = fields.Many2one('res.partner',
                                  related="sequence_id.customer_id")
    from_date = fields.Date(string="From Date")
    to_date = fields.Date(string="To Date")

    def view_report_pdf(self):
        # print("hai")
        if not self.from_date or not self.to_date:
            raise UserError(_("You must choose a From Date and To Date"))
        # prod = self.read()[0]

        data = {
            'model': 'vehicle.request',
            'form': self.read()[0]}
        prod=data['form']['vehicle_id'][0]
        print(prod)
        p = self.env['vehicle.rental'].search([('vehicle_id', '=', prod)])
        print(p)
        data['docs'] = p
        print(data)
        # used_context = self._build_contexts(data)
        # data['form']['used_context'] = dict(used_context)
        return self.env.ref(
            'vechicle_rental.report_vehicle_rental').report_action(self,
                                                                   data=data)
