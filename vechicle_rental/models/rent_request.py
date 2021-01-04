""" rent request"""
from datetime import datetime
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class RentRequest(models.Model):
    """Rent request model"""
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
                                 required=True,force_create=False)
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

    def button_confirm(self):
        """ Button confirm """
        for rec in self:
            rec.write({'state': 'confirm'})
            rec.vehicle_id.write({'state': 'notavailable'})

    def button_return(self):
        """Button return"""
        for rec in self:
            rec.write({'state': 'return'})
            rec.vehicle_id.write({'state': 'available'})

    @api.model
    def create(self, vals):
        """ Fuction to create sequnce """
        if vals.get('sequence', 'New') == 'New':
            vals['sequence'] = self.env['ir.sequence'].next_by_code(
                'vehicle.request.sequence') or 'New'
        result = super().create(vals)  # super(RentRequest, self) same
        return result

    @api.onchange('from_date', 'to_date')
    def _onchange_from_date_to_date(self):
        """Period calculation"""
        if self.from_date and self.to_date:
            if self.from_date < self.to_date:
                self.period = (self.to_date - self.from_date).days

    @api.constrains('from_date', 'to_date')
    def _constrain_from_date_to_date(self):
        """Date Validation"""
        if self.from_date and self.to_date:
            for rec in self:
                if rec.from_date > rec.to_date:
                    raise ValidationError(
                        _('Sorry, To Date Must be greater Than From Date...'))
