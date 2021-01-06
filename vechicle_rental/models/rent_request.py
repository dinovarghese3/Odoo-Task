from datetime import datetime
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
                                 required=True, force_create=False)
    from_date = fields.Date(string="From Date")
    to_date = fields.Date(string="To Date")
    period = fields.Integer(string="Period")
    state = fields.Selection(
        [('draft', 'Draft'), ('confirm', 'Confirm'),
         ('return', 'Return')],
        string='State', default='draft')
    currency_id = fields.Many2one('res.currency', string='Currency',
                                  default=lambda
                                      self: self.env.user.company_id.currency_id)
    rent = fields.Monetary(string="Rent", related='vehicle_id.rent')

    number_of_period = fields.Integer(string="Period", default=1)
    period_type = fields.Many2one('rent.charges', string="type")
    amount = fields.Monetary(string="Amount", compute='compute_amount',
                             store=True)

    @api.onchange('vehicle_id')
    def _onchange_period_type(self):
        for rec in self:
            return {'domain': {
                'period_type': [('vehicle_id', '=', rec.vehicle_id.id)]}}

    @api.depends('number_of_period')
    def compute_amount(self):
        print(self.vehicle_id)
        print(self.vehicle_id.rent_charges_ids)
        self.write(
            {'amount': self.period_type.amount * self.number_of_period})

    def button_confirm(self):
        """ Button confirm """
        for rec in self:
            rec.write({'state': 'confirm'})
            rec.vehicle_id.write({'state': 'notavailable'})
            print(rec.vehicle_id.all_request_ids)
            rec.vehicle_id.write({'all_request_ids': self})

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
        result = super().create(vals)  # super(RentRequest, self) same
        return result

    @api.onchange('from_date', 'to_date')
    def _onchange_from_date_to_date(self):
        """Period calculation"""
        if self.from_date and self.to_date:
            if self.from_date <= self.to_date:
                self.period = (self.to_date - self.from_date).days + 1

    @api.constrains('from_date', 'to_date')
    def _constrain_from_date_to_date(self):
        """Date Validation"""
        if self.from_date and self.to_date:
            for rec in self:
                if rec.from_date > rec.to_date:
                    raise ValidationError(
                        _('Sorry, To Date Must be greater Than From Date...'))
