# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
import re

class FormulierCustomerType(models.Model):

    _name = 'formulier.customer.type'
    _description = 'formulier customer type add many2many on user form'

    name = fields.Char('Name')
    technical_name = fields.Char('Technical Name')

class ResUsers(models.Model):
    """ Add new fieds on user form """

    _inherit = "res.users"

    customer_type = fields.Many2many('formulier.customer.type', string="Quotation Type")
    template_id = fields.Many2many('sale.order.template', string='Quotation Template')
    lead_category = fields.Many2one("lead.category", string="Lead Category")
    lead_lead_source = fields.Many2one("lead.source", string="Lead Source")

class ProductProduct(models.Model):
    """ add priority field for sorting products"""

    _inherit = "product.template"

    priority = fields.Integer(string='Priority')
    product_type = fields.Selection([],string='PF quote type')