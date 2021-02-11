from odoo import models, fields
from odoo.tools.safe_eval import datetime


class TopSellingFinder(models.Model):
    _inherit = 'product.template'

    sold_qty = fields.Integer("Sold Quantity")

    def change_sold_qty(self):
        date = fields.Date.today()
        date_start = fields.Date.today() - datetime.timedelta(days=7)
        # print("mmmmm")
        orders = self.env['sale.order'].search(
            [('date_order', '<=', date), ('date_order', '>=', date_start),
             ('website_id', '!=', False),
             ('state', 'in', ('sent', 'sale', 'done'))])
        # print("???????????")
        for i in orders:
            print(i.order_line)
            order_line = i.order_line
            for p in order_line:
                if p.product_id.sold_qty is not 0:
                    p.product_id.sold_qty = p.product_id.sold_qty + p.product_uom_qty
                    # print(p.product_id.name)
                    # print("qnt", p.product_id.sold_qty)
                else:
                    p.product_id.sold_qty = p.product_uom_qty
                    # print(i.name)
                    # print("qnt", p.product_id.sold_qty)
