# -*- coding: utf-8 -*-
# from odoo import http


# class PosProductVideo(http.Controller):
#     @http.route('/pos_product_video/pos_product_video/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/pos_product_video/pos_product_video/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('pos_product_video.listing', {
#             'root': '/pos_product_video/pos_product_video',
#             'objects': http.request.env['pos_product_video.pos_product_video'].search([]),
#         })

#     @http.route('/pos_product_video/pos_product_video/objects/<model("pos_product_video.pos_product_video"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('pos_product_video.object', {
#             'object': obj
#         })
