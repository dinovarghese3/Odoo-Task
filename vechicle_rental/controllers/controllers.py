# -*- coding: utf-8 -*-
from odoo import http


# class VechicleRental(http.Controller):
#     @http.route('/vechicle_rental/vech  icle_rental/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"
#
#     @http.route('/vechicle_rental/vechicle_rental/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('vechicle_rental.listing', {
#             'root': '/vechicle_rental/vechicle_rental',
#             'objects': http.request.env['vechicle_rental.vechicle_rental'].search([]),
#         })
#
#     @http.route('/vechicle_rental/vechicle_rental/objects/<model("vechicle_rental.vechicle_rental"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('vechicle_rental.object', {
#             'object': obj
#         })
