# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
import re

class ProductBrand(models.Model):
    """ product brand """

    _name = "product.brand"
    _description = "Product brand for Optimisers and converter type product"

    name = fields.Char('Brand')

class SolarProductType(models.Model):
    """ Solar product type """

    _name = "solar.type"
    _description = "Solar product type"

    name = fields.Char('Solar Type')

class ProductTemplate(models.Model):
    """ Product Template """

    _inherit = "product.template"

    product_type = fields.Selection(selection_add=[
        ('Solar Panel', 'Solar Panel'),
        ('Converter', 'Converter'),
        ('Discount', 'Discount'),
        ('Flat Roof', 'Flat Roof'),
        ('Slanted Roof', 'Slanted Roof'),
        ('Mix Roof', 'Mix Roof'),
        ('Optimisers', 'Optimisers'),
        ('Stekkers', 'Stekkers'),
        ('Overige Materialen', 'Overige Materialen'),
        ('BTW teruggave', 'BTW teruggave')],
        string='PF quote type')
    min_product_range = fields.Float(string="Minimum Range")
    max_product_range = fields.Float(string="Maximum Range")
    solar_type = fields.Many2many('solar.type', string="Solar type")
    product_brand = fields.Many2one('product.brand', string="Brand")
