from odoo import models, fields, api


class VehicleRentReporting(models.Model):
    _name = 'report.vechicle_rental.rental_report'

    # sequence_id = fields.Many2one('vehicle.request')
    vehicle_id = fields.Many2one('vehicle.rental', )
    # customer_id = fields.Many2one('res.partner',
    #                               related="sequence_id.customer_id")
    from_date = fields.Date(string="From Date")
    to_date = fields.Date(string="To Date")

    def view_report_pdf(self):
        print(self)
        data = {
            'model_id': self.id,

        }
        print(self.id)
        # used_context = self._build_contexts(data)
        # data['form']['used_context'] = dict(used_context)
        return self.env.ref(
            'vechicle_rental.print_report_pdf').report_action(self,
                                                              data=data)

    @api.model
    def _get_report_values(self, docids, data):
        print("Hallo report")
        model_id = data['model_id']
        print(model_id)
        value = []
        query = """SELECT request.vehicle_id,request.customer_id,rental.model,
        rental.vehicle_id,request.from_date,request.to_date,request.state
        FROM vehicle_request as request INNER JOIN vehicle_rental as 
        rental ON request.vehicle_id = request.vehicle_id """
        value.append(model_id)
        self._cr.execute(query, value)
        record = self._cr.dictfetchall()
        print(record)
        # print(data['vehicle_id'])
        return {
            'docs': record,
            'date_today': fields.Datetime.now(),
        }
