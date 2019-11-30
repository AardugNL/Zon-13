# -*- coding: utf-8 -*-

from odoo import models, fields


class Lead_Source(models.Model):
    _name = "lead.source"
    _description = 'Lead Source'

    name = fields.Char(string="Lead Source")

class Crm_Lead(models.Model):
    _inherit = "crm.lead"

    lead_lead_source = fields.Many2one("lead.source", string="Lead Source")

class Sale_Order(models.Model):
    _inherit = "sale.order"

    lead_lead_source = fields.Many2one("lead.source", string="Lead Source")