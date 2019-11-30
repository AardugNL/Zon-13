# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    cost_4_hours = fields.Integer("4 Hours Cost Price", default=150)
    sale_4_hours = fields.Integer(string="4 Hours Sales Price", default=200)
    cost_8_hours = fields.Integer(string="8 Hours Cost Price", default=300)
    sale_8_hours = fields.Integer(string="8 Hours Sales Price", default=375)
    cost_12_hours = fields.Integer(string="12 Hours Cost Price", default=450)
    sale_12_hours = fields.Integer(string="12 Hours Sales Price", default=565)
    cost_16_hours = fields.Integer(string="16 Hours Cost Price", default=600)
    sale_16_hours = fields.Integer(string="16 Hours Sales Price", default=750)
    cost_24_hours = fields.Integer(string="24 Hours Cost Price", default=900)
    sale_24_hours = fields.Integer(string="24 Hours Sales Price", default=1125)
    cost_30_hours = fields.Integer(string="30 Hours Cost Price", default=1050)
    sale_30_hours = fields.Integer(string="30 Hours Sales Price", default=1300)
    cost_32_hours = fields.Integer(string="32 Hours Cost Price", default=1200)
    sale_32_hours = fields.Integer(string="32 Hours Sales Price", default=1500)
    cost_36_hours = fields.Integer(string="36 Hours Cost Price", default=1350)
    sale_36_hours = fields.Integer(string="36 Hours Sales Price", default=1650)
    cost_40_hours = fields.Integer(string="40 Hours Cost Price", default=1500)
    sale_40_hours = fields.Integer(string="40 Hours Sales Price", default=1875)

    high_range =  fields.Integer(string="High", default=1000)
    middle_range =  fields.Integer(string="Middle", default=500)
    basic_range =  fields.Integer(string="Basic", default=200)
    low_range =  fields.Integer(string="Low", default=0)

class FormulierConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    cost_4_hours = fields.Integer("4 Hours Cost Price", related='company_id.cost_4_hours', readonly=False)
    sale_4_hours = fields.Integer(string="4 Hours Sales Price", related='company_id.sale_4_hours', readonly=False)
    cost_8_hours = fields.Integer(string="8 Hours Cost Price", related='company_id.cost_8_hours', readonly=False)
    sale_8_hours = fields.Integer(string="8 Hours Sales Price", related='company_id.sale_8_hours', readonly=False)
    cost_12_hours = fields.Integer(string="12 Hours Cost Price", related='company_id.cost_12_hours', readonly=False)
    sale_12_hours = fields.Integer(string="12 Hours Sales Price", related='company_id.sale_12_hours', readonly=False)
    cost_16_hours = fields.Integer(string="16 Hours Cost Price", related='company_id.cost_16_hours', readonly=False)
    sale_16_hours = fields.Integer(string="16 Hours Sales Price", related='company_id.sale_16_hours', readonly=False)
    cost_24_hours = fields.Integer(string="24 Hours Cost Price", related='company_id.cost_24_hours', readonly=False)
    sale_24_hours = fields.Integer(string="24 Hours Sales Price", related='company_id.sale_24_hours', readonly=False)
    cost_30_hours = fields.Integer(string="30 Hours Cost Price", related='company_id.cost_30_hours', readonly=False)
    sale_30_hours = fields.Integer(string="30 Hours Sales Price", related='company_id.sale_30_hours', readonly=False)
    cost_32_hours = fields.Integer(string="32 Hours Cost Price", related='company_id.cost_32_hours', readonly=False)
    sale_32_hours = fields.Integer(string="32 Hours Sales Price", related='company_id.sale_32_hours', readonly=False)
    cost_36_hours = fields.Integer(string="36 Hours Cost Price", related='company_id.cost_36_hours', readonly=False)
    sale_36_hours = fields.Integer(string="36 Hours Sales Price", related='company_id.sale_36_hours', readonly=False)
    cost_40_hours = fields.Integer(string="40 Hours Cost Price", related='company_id.cost_40_hours', readonly=False)
    sale_40_hours = fields.Integer(string="40 Hours Sales Price", related='company_id.sale_40_hours', readonly=False)

    high_range =  fields.Integer(string="High", related='company_id.high_range', readonly=False)
    middle_range =  fields.Integer(string="Middle", related='company_id.middle_range', readonly=False)
    basic_range =  fields.Integer(string="Basic", related='company_id.basic_range', readonly=False)
    low_range =  fields.Integer(string="Low", related='company_id.low_range', readonly=False)
