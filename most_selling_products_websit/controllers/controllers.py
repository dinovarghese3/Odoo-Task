""" Top selling product and Most Visited product.
 Controller to show the Top selling product and most visited product on Home page
 """

from odoo.addons.portal.controllers.web import Home
from odoo import http, fields, models
from odoo.http import request
from odoo.tools.safe_eval import datetime

"""Class to show the product on Home page """


class WebsiteSort(Home):
    list_of_product = []

    @http.route(auth='public', website=True)
    def index(self, **kw):
        super(WebsiteSort, self).index()
        # self.set_quantity()
        products = request.env['product.template'].sudo().search([])
        for each in products:
            each.sold_qty = 0
            each.no_of_view = 0
            each.top_selling = False
            each.most_visited = False

        date = fields.Date.today()
        date_start = fields.Date.today() - datetime.timedelta(days=7)

        orders = request.env['sale.order'].sudo().search(
            [('date_order', '<=', date),
             ('date_order', '>=',
              date_start),
             ('website_id', '!=', False),
             ('state', 'in',
              ('sale', 'done', 'sent'))])

        for order in orders:
            order_line = order.order_line
            for product in order_line:
                product.product_id.sold_qty = product.product_id.sold_qty + 1

        products_vist = request.env['website.track'].sudo().search(
            [('visit_datetime', '<=', date),
             ('visit_datetime', '>=', date_start),
             ('product_id', '!=', False)])
        print("product visit", products_vist)
        for pro in products_vist:
            # print(pro)
            pro.product_id.no_of_view = pro.product_id.no_of_view + 1

        website_most_selle_product_ids = request.env[
            'product.template'].sudo().search(
            [('sold_qty', '>', 0)], order='sold_qty desc', limit=8)
        for each in website_most_selle_product_ids:
            each.top_selling = True
        products_most_vist = request.env['product.template'].sudo().search(
            [('is_published', '=', True),
             ('no_of_view', '>', 0)], order='no_of_view desc', limit=8)
        for each in products_most_vist:
            each.most_visited = True

        return request.render('website.homepage', {
            'website_most_selle_product_ids': website_most_selle_product_ids,
            'products_most_vist': products_most_vist
        })
