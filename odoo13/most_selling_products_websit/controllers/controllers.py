from odoo import http
from odoo.http import request


class MostSale(http.Controller):
    @http.route('/products', type='http', auth='public', website=True)
    def most_sale_detsils(self, **kwargs):
        print("hai")
        # sale_details = request.env['sale.order'].sudo().search([])
        # return request.render('most_selling_products_websit.most_product',
        #                       {'my_details': sale_details})
