from odoo import fields, models, _, api
from odoo.exceptions import UserError, ValidationError
import json
from odoo.tools import date_utils, io

try:

    from odoo.tools.misc import xlsxwriter

except ImportError:

    import xlsxwriter


class VehicleRentReport(models.TransientModel):
    _name = 'vehicle.report'

    vehicle_id = fields.Many2one('vehicle.rental')
    from_date = fields.Date('From Date')
    to_date = fields.Date('To Date')

    def view_report_pdf(self):
        if self.from_date and self.to_date and self.from_date > self.to_date:
            raise ValidationError('From Date must be less than End Date')
        data = {
            'model_id': self.id,
            'from_date': self.from_date,
            'to_date': self.to_date,
            'vehicle_id': self.vehicle_id.name,
            've_id': self.vehicle_id.id,
        }
        print(self.id)
        return self.env.ref(
            'vechicle_rental.print_report_pdf').report_action(self,
                                                              data=data)
    def print_xlsx(self):
        # print("xls work")
        data = {
            'model_id': self.id,
            'from_date': self.from_date,
            'to_date': self.to_date,
            'vehicle_id': self.vehicle_id.name,
            've_id': self.vehicle_id.id,
        }
        return {
            'type': 'ir.actions.report',
            'data': {'model': 'vehicle.report',
                     'options': json.dumps(data, default=date_utils.json_default),
                     'output_format': 'xlsx',
                     'report_name': 'Excel Report', },
            'report_type': 'xlsx'
        }

    def get_xlsx_report(self, data, response):
        value = []
        model_id = data['model_id']
        from_date = data['from_date']
        to_date = data['to_date']
        vehicle = data['vehicle_id']
        vehicle_id = data['ve_id']
        output = io.BytesIO()
        user_obj = self.env.user

        workbook = xlsxwriter.Workbook(output, {'in_memory': True})

        txt_right = workbook.add_format({'font_size': '9px',
                                         'align': 'right', })
        txt = workbook.add_format({'font_size': '10px', })
        heading = workbook.add_format({'font_size': '10px', 'bold': True, 'align': 'center', 'bg_color': '#d9d9d9'})

        date = workbook.add_format(
            {'num_format': 'dd/mm/yyyy', 'font_size': '9px', 'align': 'left', })

        sheet = workbook.add_worksheet()
        head = workbook.add_format({'align': 'center', 'bold': True, 'font_size': '20px', })

        sheet.merge_range('B2:C2', user_obj.company_id.name, txt)
        sheet.merge_range('B3:D3', user_obj.company_id.street, txt)
        sheet.write('B4', user_obj.company_id.city, txt)
        sheet.write('C5', user_obj.company_id.zip, txt)
        sheet.merge_range('B5:E5', user_obj.company_id.state_id.name, txt)
        sheet.merge_range('B6:C6', user_obj.company_id.country_id.name, txt)
        sheet.merge_range('B7:N8', 'Vehicle Rental', head)
        sheet.merge_range('B11:C11', 'Report Date :', txt)
        sheet.merge_range('D11:E11', fields.Date.today(), date)
        if vehicle_id:
            sheet.write('B12', 'Vehicle:', txt)
            sheet.merge_range('C12:E12', data['vehicle_id'], txt)
        if from_date:
            sheet.write('B13', 'From:', txt)
            sheet.merge_range('C13:D13', data['from_date'], date)
        if to_date:
            sheet.write('F13', 'To:', txt)
            sheet.merge_range('G13:H13', data['to_date'], date)
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
            vehicle.name as vehicle_name,
            request.to_date,request.state FROM vehicle_request as request
            INNER JOIN vehicle_rental as rental ON request.vehicle_id = rental.id  
            INNER JOIN  res_partner as partner ON request.customer_id = partner.id
            INNER JOIN fleet_vehicle as vehicle ON vehicle.id = request.vehicle_id 
            WHERE  request.request_date >='%s'""" % (from_date)
        elif from_date == False and to_date and vehicle_id == False:
            query = """SELECT request.vehicle_id,request.customer_id,partner.name,
            request.request_date,rental.model,rental.vehicle_id,request.from_date,
            vehicle.name as vehicle_name,
            request.to_date,request.state FROM vehicle_request as request
            INNER JOIN vehicle_rental as rental ON request.vehicle_id = rental.id  
            INNER JOIN  res_partner as partner ON request.customer_id = partner.id 
            INNER JOIN fleet_vehicle as vehicle ON vehicle.id = request.vehicle_id
            WHERE  request.request_date <='%s'""" % (to_date)
        elif vehicle_id == False and from_date and to_date:
            query = """SELECT request.vehicle_id,request.customer_id,partner.name,
            request.request_date,rental.model,rental.vehicle_id,request.from_date,
            vehicle.name as vehicle_name,
            request.to_date,request.state FROM vehicle_request as request
            INNER JOIN vehicle_rental as rental ON request.vehicle_id = rental.id  
            INNER JOIN  res_partner as partner ON request.customer_id = partner.id 
            INNER JOIN fleet_vehicle as vehicle ON vehicle.id = request.vehicle_id
            WHERE request.request_date BETWEEN'%s' AND '%s' """ % (
                from_date, to_date)
        else:
            query = """SELECT request.vehicle_id,request.customer_id,partner.name,
            request.request_date,rental.model,rental.vehicle_id,request.from_date,
            vehicle.name as vehicle_name,
            request.to_date,request.state FROM vehicle_request as request
            INNER JOIN vehicle_rental as rental ON request.vehicle_id = rental.id  
            INNER JOIN  res_partner as partner ON request.customer_id = partner.id
            INNER JOIN fleet_vehicle as vehicle ON vehicle.id = request.vehicle_id 
             """
        value.append(model_id)
        self._cr.execute(query, value)
        record = self._cr.dictfetchall()
        if vehicle_id:
            sheet.write('B15', 'SL No', heading)
            sheet.write('D15', 'Customer', heading)
            sheet.write('F15', 'Model', heading)
            sheet.merge_range('G15:H15', 'From Date', heading)
            sheet.merge_range('I15:J15', 'To Date', heading)
            sheet.write('K15', 'State', heading)
            row_no = 15
            col_no = 1
            i = 1
            for rec in record:
                sheet.write(row_no, col_no, i, txt_right)
                sheet.merge_range(row_no, col_no + 1, row_no, col_no + 3,
                                  rec['name'], txt)

                sheet.write(row_no, col_no + 4, rec['model'], txt)
                sheet.merge_range(row_no, col_no + 5, row_no, col_no + 6, rec['from_date'], date)
                sheet.merge_range(row_no, col_no + 7, row_no, col_no + 8, rec['to_date'], date)
                sheet.write(row_no, col_no + 9, rec['state'], txt)
                row_no += 1
                i += 1
        else:
            sheet.write('B15', 'SL No', heading)
            sheet.merge_range('C15:E15', 'Vehicle', heading)
            sheet.merge_range('F15:H15', 'Customer', heading)
            sheet.write('I15', 'Model', heading)
            sheet.merge_range('J15:K15', 'From Date', heading)
            sheet.merge_range('L15:M15', 'To Date', heading)
            sheet.write('N15', 'State', heading)
            row_no = 15
            col_no = 1
            i = 1
            for rec in record:
                sheet.write(row_no, col_no, i, txt_right)
                sheet.merge_range(row_no, col_no + 1, row_no, col_no + 3, rec['vehicle_name'], txt)
                sheet.merge_range(row_no, col_no + 4, row_no, col_no + 6,
                                  rec['name'], txt)

                sheet.write(row_no, col_no + 7, rec['model'], txt)
                sheet.merge_range(row_no, col_no + 8, row_no, col_no + 9, rec['from_date'], date)
                sheet.merge_range(row_no, col_no + 10, row_no, col_no + 11, rec['to_date'], date)
                sheet.write(row_no, col_no + 12, rec['state'], txt)
                row_no += 1
                i += 1

        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
