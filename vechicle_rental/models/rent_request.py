from datetime import datetime

from addons.hw_escpos.escpos import exceptions
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class RentRequest(models.Model):
    _name = 'vehicle.request'
    _description = "All Rent requests"
    _rec_name = 'sequence'
    sequence = fields.Char(string="Request Number", readonly=True,
                           required=True, copy=False, index=True,
                           default=lambda self: _('New'))
    customer_id = fields.Many2one('res.partner', String="Customer",
                                  required=True)
    request_date = fields.Date(string="Request Date", default=datetime.today())
    vehicle_id = fields.Many2one('vehicle.rental', string="Vehicle",
                                 domain=[('state', '=', 'available')],
                                 required=True)
    from_date = fields.Date(string="From Date")
    to_date = fields.Date(string="To Date")
    period = fields.Integer(string="Period")
    state = fields.Selection(
        [('draft', 'Draft'), ('confirm', 'Confirm'),
         ('return', 'Return')],
        string='State', default='draft')
    currency_id = fields.Many2one('res.currency', string='Currency',
                                  default=lambda
                                      self: self.env.user.company_id.id)
    rent = fields.Monetary(string="Rent", related='vehicle_id.rent')

    def action_confirm(self):
        print("hai")
        for rec in self:
            rec.state = 'confirm'

    @api.model
    def create(self, vals):
        if vals.get('sequence', 'New') == 'New':
            vals['sequence'] = self.env['ir.sequence'].next_by_code(
                'vehicle.request.sequence') or 'New'
        result = super(RentRequest, self).create(vals)
        return result

    @api.onchange('from_date', 'to_date')
    def _onchange_from_date_to_date(self):
        if self.from_date and self.to_date:
            for rec in self:
                if rec.from_date < rec.to_date:
                    rec.period = (rec.to_date - rec.from_date).days

    @api.constrains('from_date', 'to_date')
    def _constrain_from_date_to_date(self):
        if self.from_date and self.to_date:
            for rec in self:
                if rec.from_date > rec.to_date:
                    raise ValidationError(
                        _('Sorry, To Date Must be greater Than From Date...'))
