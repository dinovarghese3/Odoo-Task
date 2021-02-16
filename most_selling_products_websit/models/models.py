from odoo import models, fields


class TopSellingFinder(models.Model):
    _inherit = 'product.template'

    sold_qty = fields.Integer("Sold Quantity")
    top_selling = fields.Boolean("Top Selling")
    no_of_view = fields.Integer("Number of View")
    most_visited = fields.Boolean("Most visited")
