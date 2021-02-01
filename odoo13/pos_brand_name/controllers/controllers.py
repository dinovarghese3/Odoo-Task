# -*- coding: utf-8 -*-
# from odoo import http


# class PosBrandName(http.Controller):
#     @http.route('/pos_brand_name/pos_brand_name/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/pos_brand_name/pos_brand_name/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('pos_brand_name.listing', {
#             'root': '/pos_brand_name/pos_brand_name',
#             'objects': http.request.env['pos_brand_name.pos_brand_name'].search([]),
#         })

#     @http.route('/pos_brand_name/pos_brand_name/objects/<model("pos_brand_name.pos_brand_name"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('pos_brand_name.object', {
#             'object': obj
#         })
