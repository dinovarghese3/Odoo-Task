from unittest import result

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class RentRequest(models.Model):
    _name = 'vehicle.request'
    _description = "Rent requests"
    _rec_name = 'sequence'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    sequence = fields.Char(string="Request Number", readonly=True,
                           required=True, copy=False, index=True,
                           default=lambda self: _('New'))
    customer_id = fields.Many2one('res.partner', String="Customer",
                                  required=True)
    request_date = fields.Date(string="Request Date",
                               default=fields.date.today())
    vehicle_id = fields.Many2one('vehicle.rental', string="Vehicle",
                                 track_visibility='onchange',
                                 domain=[('state', '=', 'available')],
                                 required=True, force_create=False)
    from_date = fields.Date(string="From Date", track_visibility='onchange')
    to_date = fields.Date(string="To Date", track_visibility='always')
    period = fields.Integer(string="Period")
    state = fields.Selection(
        [('draft', 'Draft'), ('confirm', 'Confirm'),
         ('return', 'Return')],
        string='State', default='draft', track_visibility='onchange')
    currency_id = fields.Many2one('res.currency', string='Currency',
                                  default=lambda
                                      self: self.env.user.company_id.currency_id)
    rent = fields.Monetary(string="Rent", related='period_type.amount')

    number_of_period = fields.Integer(string="Period", default=1)
    period_type = fields.Many2one('rent.charges', string="type",
                                  track_visibility='onchange')
    amount = fields.Monetary(string="Amount", store=True,
                             compute='compute_amount_period_type',
                             track_visibility='onchange')

    @api.onchange('vehicle_id')
    def _onchange_period_type(self):
        for rec in self:
            return {'domain': {
                'period_type': [('vehicle_id', '=', rec.vehicle_id.id)]}}

    @api.depends('number_of_period', 'period_type')
    def compute_amount_period_type(self):
        # print(self.vehicle_id)
        # print(self.vehicle_id.rent_charges_ids)
        self.write(
            {'amount': self.period_type.amount * self.number_of_period})

    def button_confirm(self):
        """ Button confirm """
        for rec in self:
            rec.write({'state': 'confirm'})
            rec.vehicle_id.write({'state': 'not_available'})
            # print(rec.vehicle_id.all_request_ids)
            # return {'domain': {'all_request_ids': self.id}}
            # return dict(domain={'check_id': self.id})

    def button_return(self):
        """Button return"""
        for rec in self:
            rec.write({'state': 'return'})
            rec.vehicle_id.write({'state': 'available'})

    @api.model
    def create(self, vals):
        """ Function to create sequence """
        if vals.get('sequence', 'New') == 'New':
            vals['sequence'] = self.env['ir.sequence'].next_by_code(
                'vehicle.request.sequence') or 'New'
                        # super(RentRequest, self) same
        return super().create(vals)

    @api.onchange('from_date', 'to_date')
    def _onchange_from_date_to_date(self):
        """Period calculation"""
        if self.from_date and self.to_date and (self.from_date <= self.to_date):
            self.period = (self.to_date - self.from_date).days + 1

    @api.constrains('from_date', 'to_date')
    def _constrain_from_date_to_date(self):
        """Date Validation"""
        for rec in self.filtered(
                lambda l: l.from_date and l.to_date and (
                        l.from_date > l.to_date)):
            raise ValidationError(
                _('Sorry, To Date Must be greater Than From Date...'))
