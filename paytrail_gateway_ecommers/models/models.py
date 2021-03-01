import base64
import hashlib
import string
from datetime import datetime
import random

from Crypto.Cipher import AES
from werkzeug import urls

from odoo import models, fields, api

import logging
import hmac

_logger = logging.getLogger(__name__)


class Paytrail_gateway(models.Model):
    _inherit = 'payment.acquirer'
    provider = fields.Selection(selection_add=[('paytrail', 'Paytrail')],
                                ondelete={'paytrail': 'set '
                                                      'default'})
    # MERCHANT_ID
    paytrail_merchant_id = fields.Char('Merchant ID',
                                       required_if_provider='Paytrail',
                                       groups='base.group_user')
    paytrail_merchant_key = fields.Char('Merchant Key',
                                        required_if_provider='Paytrail',
                                        groups='base.group_user')

    @api.model
    def _get_paytrail_urls(self):
        """ Atom URLS """
        # print('url')
        return {
            'paytrail_form_url': 'https://payment.paytrail.com/e2'
        }

    def paytrail_get_form_action_url(self):
        # print('action')
        return self._get_paytrail_urls()['paytrail_form_url']

    def paytrail_form_generate_values(self, values):
        self.ensure_one()
        base_url = self.env['ir.config_parameter'].sudo().get_param(
            'web.base.url')
        # print("form", base_url)
        now = datetime.now()
        merchant_key = self.paytrail_merchant_key
        print("m key", merchant_key)
        payment_id = ''
        timestamp = ''
        status = 'test'
        locale = "en_US"
        # print("dict")

        paytrail_values = dict(
            Hash='6pKF4jkv97zmqBJ3ZL8gUw5DfT2NMQ',
            MERCHANT_ID=self.paytrail_merchant_id,
            # url_success=base_url + '/payment.paytrail.com/return/',
            URL_SUCCESS=urls.url_join(base_url, '/payment/paytrail/success'),
            URL_CANCEL=urls.url_join(base_url, '/payment/paytrail/cancel'),
            ORDER_NUMBER='123456',
            # order_number1 = str(values['reference']),
            PARAMS_IN='MID, url_success, url_cancel, order_number,locale',
            LOCALE="en_US",
            PARAMS_OUT='payment_id, timestamp, status',
            AMOUNT='350',
        )
        # print("done")
        paytrail_values['AUTHCODE'] = self.generate_checksum_by_str(
            paytrail_values,
            self.paytrail_merchant_key)
        print("paytrail_values", paytrail_values)
        return paytrail_values

    def __get_param_string__(self, params, escape_refund=True):
        params_string = []
        # print("getparam")
        for key in params.keys():
            # print("key", params[key])
            if ("|" in params[key] or (
                    escape_refund == True and "REFUND" in params[key])):
                respons_dict = {}
                exit()
            value = params[key]
            # print(type(value))
            if type(value) != list:
                params_string.append('' if value == 'null' else str(value))
            else:
                params_string.append(
                    '' if value == 'null' else str(value)[1:-1])
        return '|'.join(params_string)

    #     return '6pKF4jkv97zmqBJ3ZL8gUw5DfT2NMQ|13466|http://www.example.com/success|http://www.example.com/cancel|123456|MERCHANT_ID,URL_SUCCESS,URL_CANCEL,ORDER_NUMBER,PARAMS_IN,PARAMS_OUT,ITEM_TITLE[0],ITEM_ID[0],ITEM_QUANTITY[0],ITEM_UNIT_PRICE[0],ITEM_VAT_PERCENT[0],ITEM_DISCOUNT_PERCENT[0],ITEM_TYPE[0],ITEM_TITLE[1],ITEM_ID[1],ITEM_QUANTITY[1],ITEM_UNIT_PRICE[1],ITEM_VAT_PERCENT[1],ITEM_DISCOUNT_PERCENT[1],ITEM_TYPE[1],MSG_UI_MERCHANT_PANEL,URL_NOTIFY,LOCALE,CURRENCY,REFERENCE_NUMBER,PAYMENT_METHODS,PAYER_PERSON_PHONE,PAYER_PERSON_EMAIL,PAYER_PERSON_FIRSTNAME,PAYER_PERSON_LASTNAME,PAYER_COMPANY_NAME,PAYER_PERSON_ADDR_STREET,PAYER_PERSON_ADDR_POSTAL_CODE,PAYER_PERSON_ADDR_TOWN,PAYER_PERSON_ADDR_COUNTRY,VAT_IS_INCLUDED,ALG|ORDER_NUMBER,PAYMENT_ID,AMOUNT,CURRENCY,PAYMENT_METHOD,TIMESTAMP,STATUS|Product 101|101|2|300.00|15.00|50|1|Product 202|202|4|12.50|0|0|1|Order 123456|http://www.example.com/notify|en_US|EUR|REF-0001|1|01234567890|john.doe@example.com|John|Doe|Test Company|Test Street 1|608009|Test Town|AA|1|1'

    def generate_checksum_by_str(self, param_str, merchant_key, salt=None):
        # IV = "@@@@&&&&####$$$$".encode()
        params_string = self.__get_param_string__(param_str)
        print(params_string)
        # p="6pKF4jkv97zmqBJ3ZL8gUw5DfT2NMQ|13466|http://www.example.com/success|http://www.example.com/cancel|123456|MERCHANT_ID,URL_SUCCESS,URL_CANCEL,ORDER_NUMBER,PARAMS_IN,PARAMS_OUT,AMOUNT|PAYMENT_ID,TIMESTAMP,STATUS|350.00"
        hasher = hashlib.sha256(params_string.encode("UTF-8"))
        # print("p", p)
        # hasher = hashlib.sha256(p.encode("UTF-8"))
        hash_string = hasher.hexdigest()
        hash = hash_string.upper()
        print("hasher", hash)
        return hash
