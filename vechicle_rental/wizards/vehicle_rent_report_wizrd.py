from odoo import fields, models, _, api
from odoo.exceptions import UserError
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
        # print(self)
        data = {
            'model_id': self.id,
            'from_date': self.from_date,
            'to_date': self.to_date,
            'vehicle_id': self.vehicle_id.name,
            've_id': self.vehicle_id.id,
        }
        print(self.id)
        # used_context = self._build_contexts(data)
        # data['form']['used_context'] = dict(used_context)
        return self.env.ref(
            'vechicle_rental.print_report_pdf').report_action(self,
                                                              data=data)

    def print_xlsx(self):
        print("xls work")
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
        print("Hai")
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet()
        cell_format = workbook.add_format({'font_size': '12px'})
        head = workbook.add_format({'align': 'center', 'bold': True, 'font_size': '20px'})
        txt = workbook.add_format({'font_size': '10px'})
        sheet.merge_range('B2:I3', 'EXCEL REPORT', head)
        sheet.write('B6', 'From:', cell_format)
        sheet.merge_range('C6:D6', data['start_date'], txt)
        sheet.write('F6', 'To:', cell_format)
        sheet.merge_range('G6:H6', data['end_date'], txt)
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
