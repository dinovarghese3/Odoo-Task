from odoo import models, fields


class TopSellingFinder(models.Model):
    _inherit = 'product.template'

    sold_qty = fields.Integer("Sold Quantity")
    top_selling = fields.Boolean("Top Selling")
    no_of_view = fields.Integer("Number of View")
    most_visited = fields.Boolean("Mostvisited")

    # def initialize_all(self):
    #     products = self.env['product.template'].search([])
    #     for each in products:
    #         each.sold_qty = 0
    #         each.no_of_view = 0
    #         each.top_selling = False
    #         each.most_visited = False
    # def qnt_update(self,orders,products_vist):
    #     for order in orders:
    #         order_line = order.order_line
    #         for product in order_line:
    #             # product.product_id.qty_sold == 0
    #             # print(product.product_id.sold_qty)
    #             product.product_id.sold_qty = product.product_id.sold_qty + 1
    #     for product in products_vist:
    #         product.product_id.no_of_view = product.product_id.no_of_view + 1
#
#     def change_sold_qty(self):
#         date = fields.Date.today()
#         date_start = fields.Date.today() - datetime.timedelta(days=7)
#         orders = self.env['sale.order'].search(
#             [('date_order', '<=', date), ('date_order', '>=', date_start),
#              ('website_id', '!=', False),
#              ('state', 'in', ('sent', 'sale', 'done'))])
#         for i in orders:
#             print(i.order_line)
#             order_line = i.order_line
#             for p in order_line:
#                 if p.product_id.sold_qty is not 0:
#                     p.product_id.sold_qty = 0
#                     p.product_id.sold_qty = p.product_id.sold_qty + p.product_uom_qty
#                     # print(p.product_id.name)
#                     # print("qnt", p.product_id.sold_qty)
#                 else:
#                     p.product_id.sold_qty = p.product_uom_qty
#                     # print(i.name)
#                     # print("qnt", p.product_id.sold_qty)
