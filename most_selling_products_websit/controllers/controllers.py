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
        list_ids = request.env['product.template'].search(
            [('is_published', '=', True)])
        website_most_selle_product_ids = request.env['product.template'].search(
            [('sold_qty', '>', 0)])
        return request.render('website.homepage', {
            'website_most_selle_product_ids': website_most_selle_product_ids, 'list_ids': list_ids
        })
    #
    # def top_selling_product(self):
    #     date = fields.Date.today()
    #     date_start = fields.Date.today() - datetime.timedelta(days=7)
    #
    #     orders = request.env['product.template'].search([('sold_qty', '>', 0)])
    #     for i in orders:
    #         # orderline = i.order_line
    #         # for j in orderline:
    #         self.list_of_product.append(i)
    #         print(i)
    #     return self.list_of_product
