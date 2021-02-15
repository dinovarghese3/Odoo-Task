from odoo.addons.portal.controllers.web import Home
from odoo import http, fields, models
from odoo.http import request
from odoo.tools.safe_eval import datetime


class WebsiteSort(Home):
    list_of_product = []

    @http.route(auth='public')
    def index(self, **kw):
        super(WebsiteSort, self).index()
        # self.set_quantity()
        products = request.env['product.template'].search([])
        for each in products:
            each.sold_qty = 0
            each.no_of_view
            each.top_selling = False
            each.most_visited = False
            no_of_view = 0
        date = fields.Date.today()
        date_start = fields.Date.today() - datetime.timedelta(days=7)

        orders = request.env['sale.order'].search([('date_order', '<=', date),
                                                   ('date_order', '>=',
                                                    date_start),
                                                   ('website_id', '!=', False),
                                                   ('state', 'in',
                                                    ('sale', 'done', 'sent'))])

        for order in orders:
            order_line = order.order_line
            for product in order_line:
                product.product_id.sold_qty = product.product_id.sold_qty + 1

        products_vist = request.env['website.track'].search(
            [('visit_datetime', '<=', date),
             ('visit_datetime', '>=', date_start),
             ('product_id', '!=', False)])
        for product in products_vist:
            product.product_id.no_of_view = product.product_id.no_of_view + 1

        website_most_selle_product_ids = request.env['product.template'].search(
            [('sold_qty', '>', 0)], order='sold_qty desc', limit=8)
        for each in website_most_selle_product_ids:
            each.top_selling = True
        products_most_vist = request.env['product.template'].search(
            [('is_published', '=', True),
             ('no_of_view', '!=', 0)], order='no_of_view desc', limit=8)
        for each in products_most_vist:
            each.most_visited = True

        return request.render('website.homepage', {
            'website_most_selle_product_ids': website_most_selle_product_ids,
            'products_most_vist': products_most_vist
        })


