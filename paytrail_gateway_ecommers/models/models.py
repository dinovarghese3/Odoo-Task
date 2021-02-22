# -*- coding: utf-8 -*-

from odoo import models, fields, api


class paytrail_gateway_ecommerce(models.Model):
    _inherit = 'payment.acquirer'
    provider = fields.Selection(selection_add=[('paytrail', 'Paytrail')],
                                ondelete={'paytrail': 'set '
                                                      'default'})
