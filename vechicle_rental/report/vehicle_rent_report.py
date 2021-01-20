from odoo import models, fields, api


class ReportVehicleRent(models.AbstractModel):
    _name = 'report.vechicle_rental.report'

    # sequence_id = fields.Many2one('vehicle.request')
    vehicle_id = fields.Many2one('vehicle.rental', )
    # customer_id = fields.Many2one('res.partner',
    #                               related="sequence_id.customer_id")
    from_date = fields.Date(string="From Date")
    to_date = fields.Date(string="To Date")

    def view_report_pdf(self):
        data = {
            'model_id': self.id
        }
        print(data)
        # used_context = self._build_contexts(data)
        # data['form']['used_context'] = dict(used_context)
        return self.env.ref(
            'vechicle_rental.report_vehicle_rental').report_action(self,
                                                                   data=data)

    @api.model
    def _get_report_values(self, docids, data):
        print("Hallo report")
        model_id = data['model_id']
        value = []
        query = """SELECT *
                    	FROM vehicle_request"""
        value.append(model_id)
        self._cr.execute(query, value)
        record = self._cr.dictfetchall()
        return {
            'docs': record,
            'date_today': fields.Datetime.now(),
        }
