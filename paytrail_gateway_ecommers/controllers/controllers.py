# -*- coding: utf-8 -*-
# from odoo import http


# class PaytrailGatewayEcommers(http.Controller):
#     @http.route('/paytrail_gateway_ecommers/paytrail_gateway_ecommers/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/paytrail_gateway_ecommers/paytrail_gateway_ecommers/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('paytrail_gateway_ecommers.listing', {
#             'root': '/paytrail_gateway_ecommers/paytrail_gateway_ecommers',
#             'objects': http.request.env['paytrail_gateway_ecommers.paytrail_gateway_ecommers'].search([]),
#         })

#     @http.route('/paytrail_gateway_ecommers/paytrail_gateway_ecommers/objects/<model("paytrail_gateway_ecommers.paytrail_gateway_ecommers"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('paytrail_gateway_ecommers.object', {
#             'object': obj
#         })
