# from idlelib import window
#
# from odoo import http, api
# from odoo.http import request
#
#
# class MostSale(http.Controller):
#     @http.route('''/''',
#                 type='http', auth='public', website=True)
#     def most_sale_detsils(self, **kwargs):
#         print("hai")
#         products = request.env['product.template'].sudo().search(
#             [('sale_ok', '=', True)])
#         for j in products:
#             print("img",j.image_1920,"\n")
#             # sale_details = request.env['sale.report'].sudo().search(
#         #         [('product_id.name', '=', j.name)])
#         #     for k in sale_details:
#         #         print(k.product_id.name)
#         #         print(k.product_uom_qty)
#
#         # for i in sale_details:
#         #     print(i.product_id.name)
#         # self.get_img_url(products)
#
#         return request.render('most_selling_products_websit.product',
#                               {'products': products})
#
#     @api.model
#     def get_values(self):
#         print("DINO>>>>>>>>>>>")
#         # Generates a random name between 9 and 15 characters long and writes it to the record.
#         # self.write({'name': ''.join(
#         #     random.SystemRandom().choice(string.ascii_uppercase + string.digits)
#         #     for _ in range(randint(9, 15)))})
#
#     # def get_most_selling_product(self):
#     #     print("Most selling product")
#     # def get_img_url(self, product):
#     #     for i in product:
#     #         print(i)

from odoo.addons.portal.controllers.web import Home
from odoo import http, fields
from odoo.http import request
from odoo.tools.safe_eval import datetime


class WebsiteSort(Home):
    list_of_product = []

    @http.route(auth='public')
    def index(self, **kw):
        super(WebsiteSort, self).index()
        list_ids = request.env['product.product'].search(
            [('is_published', '=', True)])
        website_most_selle_product_ids = request.env['product.template'].search(
            [('sold_qty', '>', 0)], order='sold_qty desc', limit=8)
        products_most_vist = set(request.env['website.track'].search(
            [('product_id.name', '!=', False)]).mapped(
            'product_id.product_tmpl_id'))
        print(products_most_vist)
        # list=[]
        for i in products_most_vist:
            print(i.id, i.name)

        # for j in list:
        #     print(j.product_id.name)

        # for i in products_most_vist:
        #     products_most = request.env['website.track'].search_count(
        #         [('product_id', '=', i.product_id.id)])
        #     print(i.product_id.name, "   ", products_most)
        return request.render('website.homepage', {
            'website_most_selle_product_ids': website_most_selle_product_ids,
            'list_ids': list_ids, 'products_most_vist': products_most_vist
        })
