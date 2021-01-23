from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class VehicleRentReporting(models.Model):
    _name = 'report.vechicle_rental.rental_report'

    # sequence_id = fields.Many2one('vehicle.request')
    # vehicle_id = fields.Many2one('vehicle.rental', )
    # customer_id = fields.Many2one('res.partner',
    #                               related="sequence_id.customer_id")
    # from_date = fields.Date(string="From Date")
    # to_date = fields.Date(string="To Date")

    @api.model
    def _get_report_values(self, docids, data):
        # print("Hallo report")
        # if data['model_id'] :
        model_id = data['model_id']
        from_date = data['from_date']
        to_date = data['to_date']
        vehicle = data['vehicle_id']
        vehicle_id = data['ve_id']
        # print(from_date)
        # print(vehicle_id)
        value = []
        # print(from_date,to_date)
        if vehicle_id and from_date and to_date:
            query = """SELECT request.vehicle_id,request.customer_id,partner.name,
            request.request_date,rental.model,rental.vehicle_id,request.from_date,
            request.to_date,request.state FROM vehicle_request as request
            INNER JOIN vehicle_rental as rental ON request.vehicle_id = rental.id  
            INNER JOIN  res_partner as partner ON request.customer_id = partner.id 
            WHERE request.vehicle_id = %s AND request.request_date BETWEEN 
            '%s' AND '%s' """ % (vehicle_id, from_date, to_date)
        elif vehicle_id and from_date == False and to_date == False:
            query = """SELECT request.vehicle_id,request.customer_id,partner.name,
            request.request_date,rental.model,rental.vehicle_id,request.from_date,
            request.to_date,request.state FROM vehicle_request as request
            INNER JOIN vehicle_rental as rental ON request.vehicle_id = rental.id  
            INNER JOIN  res_partner as partner ON request.customer_id = partner.id 
            WHERE request.vehicle_id = %s """ % (vehicle_id)
        elif vehicle_id and from_date and to_date == False:
            query = """SELECT request.vehicle_id,request.customer_id,partner.name,
            request.request_date,rental.model,rental.vehicle_id,request.from_date,
            request.to_date,request.state FROM vehicle_request as request
            INNER JOIN vehicle_rental as rental ON request.vehicle_id = rental.id  
            INNER JOIN  res_partner as partner ON request.customer_id = partner.id 
            WHERE request.vehicle_id = %s AND request.request_date >= 
            '%s'  """ % (vehicle_id, from_date)
        elif vehicle_id and from_date == False and to_date:
            query = """SELECT request.vehicle_id,request.customer_id,partner.name,
            request.request_date,rental.model,rental.vehicle_id,request.from_date,
            request.to_date,request.state FROM vehicle_request as request
            INNER JOIN vehicle_rental as rental ON request.vehicle_id = rental.id  
            INNER JOIN  res_partner as partner ON request.customer_id = partner.id 
            WHERE request.vehicle_id = %s AND request.request_date <= 
            '%s'  """ % (vehicle_id, to_date)
        elif from_date and to_date == False and vehicle_id == False:
            query = """SELECT request.vehicle_id,request.customer_id,partner.name,
            request.request_date,rental.model,rental.vehicle_id,request.from_date,
            request.to_date,request.state FROM vehicle_request as request
            INNER JOIN vehicle_rental as rental ON request.vehicle_id = rental.id  
            INNER JOIN  res_partner as partner ON request.customer_id = partner.id 
            WHERE  request.request_date >='%s'""" % (from_date)
        elif from_date == False and to_date and vehicle_id == False:
            query = """SELECT request.vehicle_id,request.customer_id,partner.name,
            request.request_date,rental.model,rental.vehicle_id,request.from_date,
            request.to_date,request.state FROM vehicle_request as request
            INNER JOIN vehicle_rental as rental ON request.vehicle_id = rental.id  
            INNER JOIN  res_partner as partner ON request.customer_id = partner.id 
            WHERE  request.request_date <='%s'""" % (to_date)
        elif vehicle_id == False and from_date and to_date:
            query = """SELECT request.vehicle_id,request.customer_id,partner.name,
            request.request_date,rental.model,rental.vehicle_id,request.from_date,
            request.to_date,request.state FROM vehicle_request as request
            INNER JOIN vehicle_rental as rental ON request.vehicle_id = rental.id  
            INNER JOIN  res_partner as partner ON request.customer_id = partner.id 
            WHERE request.request_date BETWEEN'%s' AND '%s' """ % (
                from_date, to_date)
        else:
            query = """SELECT request.vehicle_id,request.customer_id,partner.name,
            request.request_date,rental.model,rental.vehicle_id,request.from_date,
            request.to_date,request.state FROM vehicle_request as request
            INNER JOIN vehicle_rental as rental ON request.vehicle_id = rental.id  
            INNER JOIN  res_partner as partner ON request.customer_id = partner.id 
             """
        value.append(model_id)
        self._cr.execute(query, value)
        record = self._cr.dictfetchall()
        # print(record)
        # print(data['vehicle_id'])
        return {
            'docs': record,
            'date_today': fields.Date.today(),
        }
