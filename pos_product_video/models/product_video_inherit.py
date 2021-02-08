from odoo import models, fields


class ProductVideo(models.Model):
    _inherit = 'product.product'
    _description = 'Adding Video Url field to product '
    product_video_url = fields.Char(string="Product Video")


class PosCategory(models.Model):
    _inherit = 'pos.config'

    product_video = fields.Boolean(string="Product Video")
