# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductBrandInherit(models.Model):
    # _name = 'product.inherit.brand'
    _inherit = 'product.template'
    _description = 'Product Brand to POS'

    brand_name = fields.Char(string="Brand")
