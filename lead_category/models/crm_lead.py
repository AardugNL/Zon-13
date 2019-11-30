# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Lead_Category(models.Model):
    _name = "lead.category"
    _description = 'Lead Category'

    name = fields.Char(string="Lead Category")
    tag_ids = fields.Many2many('crm.lead.tag', string='Tags')


class Crm_Lead(models.Model):
    _inherit = "crm.lead"

    lead_category = fields.Many2one("lead.category", string="Lead Category")

    @api.onchange('lead_category')
    def set_tags(self):
        self.tag_ids = self.lead_category.tag_ids

class Sale_Order(models.Model):
    _inherit = "sale.order"

    lead_category = fields.Many2one("lead.category", string="Lead Category")
