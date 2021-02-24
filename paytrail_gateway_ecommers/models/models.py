# -*- coding: utf-8 -*-
import base64
import hashlib
from datetime import datetime

# from Crypto.Cipher import AES
# import AES
import requests

from odoo import models, fields, api
from odoo.service import common
from odoo.tools.safe_eval import json


class paytrail_gateway_ecommerce(models.Model):
    _inherit = 'payment.acquirer'
    provider = fields.Selection(selection_add=[('paytrail', 'Paytrail')],
                                ondelete={'paytrail': 'set '
                                                      'default'})

    paytrail_key_id = fields.Char(string='Merchant ID',
                                  required_if_provider='paytrail',
                                  groups='base.group_user')

    #
    paytrail_key_secret = fields.Char(string='Merchant Key',
                                      required_if_provider='paytrail',
                                      groups='base.group_user')

    @api.model
    def _get_paytrail_urls(self):
        """ URL """
        return {'paytrail_from_url': 'https://payment.paytrail.com/e2'}

    def paytrail_get_form_action_url(self):
        print(self._get_paytrail_urls()['paytrail_from_url'])
        return self._get_paytrail_urls()['paytrail_from_url']

    def paytrail_form_generate_values(self, values):
        print('self', self)
        self.ensure_one()
        base_url = self.env['ir.config_parameter'].sudo().get_param(
            'web.base.url')
        MID = int(self.paytrail_key_id)
        now = datetime.now()
        url_success = 'http://www.example.com/success'
        url_cancel = 'http://www.example.com/cancel'
        order_number = 123456
        merchant_key = self.paytrail_key_secret
        payment_id = ''
        timestamp = ''
        status = ''
        locale = "en_US"

        print('url', base_url, MID, merchant_key)
        print("value", values)
        paytrail_values = dict(
            MID=int(self.paytrail_key_id),

            url_success='http://www.example.com/success',
            url_cancel='http://www.example.com/cancel',

            order_number=123456,

            params_in=[MID, url_success, url_cancel, order_number, locale],
            locale="en_US",
            params_out=[payment_id, timestamp, status],
            amount='350',
        )
        paytrail_values[
            'reqHashKey'] = 'BBDF8997A56F97DC0A46C99C88C2EEF9D541AAD59CFF2695D0DD9AF474086D71'
        r = requests.post(url=self.paytrail_get_form_action_url(),
                          data=paytrail_values)
        print("rrrrrrrrrr :", r)

        paytm_values_json = json.dumps(paytrail_values, indent=2)
        return paytrail_values


class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    @api.model
    def _create_paytrail_capture(self, data):
        payment_acquirer = self.env['payment.acquirer'].search(
            [('provider', '=', 'paytrail')], limit=1)
        payment_url = "https://payment.paytrail.com/e2" % (
        payment_acquirer.paytrail_key_id, payment_acquirer.paytrail_key_secret,
        data.get('payment_id'))
        try:
            payment_response = requests.get(payment_url)
            payment_response = payment_response.json()
        except Exception as e:
            raise e
        # reference = payment_response.get('notes', {}).get('order_id', False)
        # if reference:
        #     transaction = self.search([('reference', '=', reference)])
        #     capture_url = "https://%s:%s@api.razorpay.com/v1/payments/%s/capture" % (payment_acquirer.razorpay_key_id, payment_acquirer.razorpay_key_secret, data.get('payment_id'))
        #     charge_data = {'amount': int(transaction.amount * 100)}
        #     try:
        #         payment_response = requests.post(capture_url, data=charge_data)
        #         payment_response = payment_response.json()
        #     except Exception as e:
        #         raise e
        return payment_response
