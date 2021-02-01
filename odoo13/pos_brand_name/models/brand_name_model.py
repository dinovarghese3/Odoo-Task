from odoo import models, fields


class ProductBrandNameInherit(models.Model):
    _name = 'product.brand.name'
    name = fields.Char("Brand")


class ProductBrandInherit(models.Model):
    # _name = 'product.inherit.brand'
    _inherit = 'product.product'
    _description = 'Product Brand to POS'
    _rec_name = 'name'

    brand_name_id = fields.Many2one('product.brand.name', string="Brand")
