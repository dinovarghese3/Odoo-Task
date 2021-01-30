# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductBrandInherit(models.Model):
    # _name = 'product.inherit.brand'
    _inherit = 'product.product'
    _description = 'Product Brand to POS'

    brand_name = fields.Char(string="Brand")
