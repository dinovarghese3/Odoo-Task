# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class most_selling_products_websit(models.Model):
#     _name = 'most_selling_products_websit.most_selling_products_websit'
#     _description = 'most_selling_products_websit.most_selling_products_websit'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
