from odoo import http
from odoo.http import request


class MostSale(http.Controller):
    @http.route('/products', type='http', auth='public', website=True)
    def most_sale_detsils(self, **kwargs):
        print("hai")
        products = request.env['product.template'].sudo().search(
            [('sale_ok', '=', True)])
        return request.render('most_selling_products_websit.product',
                              {'products': products})
        #                       {'my_details': sale_details})
        # return "Hai Dino"
