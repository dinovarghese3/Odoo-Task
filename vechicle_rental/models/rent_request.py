from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class RentRequest(models.Model):
    _name = 'vehicle.request'
    _description = "Rent requests"
    _rec_name = 'sequence'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    sequence = fields.Char(string="Number", readonly=True,
                           required=True, copy=False, index=True,
                           default=lambda self: _('New'))
    customer_id = fields.Many2one('res.partner', String="Customer",
                                  required=True, track_visibility='always',
                                  store=True)
    request_date = fields.Date(string="Request Date",
                               default=fields.date.today())
    vehicle_id = fields.Many2one('vehicle.rental', string="Vehicle",
                                 track_visibility='always',
                                 domain=[('state', '=', 'available')],
                                 required=True, force_create=False, store=True)
    from_date = fields.Date(string="From Date", track_visibility='always')
    to_date = fields.Date(string="To Date", track_visibility='always')
    period = fields.Integer(string="Period")
    state = fields.Selection(
        [('draft', 'Draft'), ('confirm', 'Confirm'),
         ('invoiced', 'Invoiced'),
         ('return', 'Return')],
        string='State', default='draft', track_visibility='onchange')
    currency_id = fields.Many2one('res.currency', string='Currency',
                                  default=lambda
                                      self: self.env.user.company_id.currency_id)
    rent = fields.Monetary(string="Rent", related='period_type.amount')

    number_of_period = fields.Float(string="Period", default=1)
    period_type = fields.Many2one('rent.charges', string="type",
                                  track_visibility='always')
    amount = fields.Monetary(string="Amount", store=True,
                             compute='compute_amount_period_type',
                             track_visibility='onchange')
    warning = fields.Boolean(default=False, compute='_compute_warning')
    late = fields.Boolean(default=False, compute='_compute_late')
    invoice_id = fields.Many2one('account.move')
    is_paid = fields.Boolean(compute='_compute_is_paid')

    def _compute_warning(self):
        """ Warning boolean set befor 2 days """
        for rec in self:
            rec.warning = False
            rec.warning = rec.state == 'confirm' and rec.to_date and (
                (rec.to_date - fields.Date.today()).days) <= 2

    def _compute_late(self):
        """Late boolean field set after the date """
        for rec in self:
            rec.late = False
            rec.late = rec.state == 'confirm' and rec.to_date and \
                       rec.to_date < fields.Date.today()
            if rec.late:
                rec.warning = False

    @api.onchange('vehicle_id')
    def _onchange_period_type(self):
        """ Period type getting from rent vehicle module """
        for rec in self:
            return {'domain': {
                'period_type': [('vehicle_id', '=', rec.vehicle_id.id)]}}

    @api.depends('number_of_period', 'period_type')
    def compute_amount_period_type(self):
        """ Compute amount based on period type and rent"""
        for rec in self:
            rec.write(
                {'amount': rec.period_type.amount * rec.number_of_period})

    def button_confirm(self):
        """ Button confirm state """
        if self.vehicle_id.state == "available":
            self.write({'state': 'confirm'})
            self.vehicle_id.write({'state': 'not_available'})
        else:
            raise ValidationError("This car is Not Available")

    def button_return(self):
        """Button return state"""
        self.write({'state': 'return'})
        self.vehicle_id.write({'state': 'available'})

    def button_create_invoice(self):
        """ creating invoice """
        invoice = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'date': fields.Date.today(),
            'l10n_in_gst_treatment': self.customer_id.l10n_in_gst_treatment,
            'invoice_date': self.to_date,
            'partner_id': self.customer_id.id,
            'currency_id': self.currency_id.id,
            'invoice_line_ids': [(0, 0, {
                'product_id': self.env['product.product'].search(
                    [('name', '=', 'Rent')], ),
                'name': self.vehicle_id.name,
                'price_unit': self.amount})],
        })
        invoice.action_post()
        self.invoice_id = invoice.id
        for rec in self:
            rec.write({'state': 'invoiced'})
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_type': 'form',
            'view_mode': 'form',
            'res_id': invoice.id,
            'context': "{'create': False,'edit': False}", }

    def _compute_is_paid(self):
        """ Checking the invoice is paid or not"""
        for rec in self:
            rec.is_paid = rec.invoice_id.payment_state == 'paid'

    def button_invoices_all(self):
        """ To View the invoice"""
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_type': 'form',
            'view_mode': 'form',
            'res_id': self.invoice_id.id,
            'context': "{'create': False, 'edit':False}",
        }

    @api.model
    def create(self, vals):
        """ Function to create sequence """
        if vals.get('sequence', 'New') == 'New':
            vals['sequence'] = self.env['ir.sequence'].next_by_code(
                'vehicle.request.sequence') or 'New'
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

    _sql_constraints = [
        ('unique_sequnce', 'unique(sequence)', 'Sequnce Error!'),

    ]
