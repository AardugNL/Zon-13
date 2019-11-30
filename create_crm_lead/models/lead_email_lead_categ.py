# -*- encoding: utf-8 -*-

from odoo import models, fields, api


class CRMLead(models.Model):
    _inherit = 'crm.lead'

    email_description = fields.Html('Email Description', translate=True)


class LeadEmailLeadCategory(models.Model):
    _name = 'lead.email.lead.category'
    _description = 'Email Lead Category'

    lead_category = fields.Many2one('lead.category', string='Lead Category')
    lead_email_lead_source = fields.Many2one(
        'lead.email.lead.source', string='Lead Email Lead Source')
    content = fields.Char('Content')
    priority = fields.Char('Priority')


class LeadEmailLeadSource(models.Model):
    _name = 'lead.email.lead.source'
    _description = 'Email Lead Source'

    name = fields.Char(compute='_compute_name', store=True, string='Name')
    lead_source = fields.Many2one('lead.source', string="Lead Source")
    domain = fields.Char(string='Domain')

    @api.depends('lead_source', 'lead_source.name', 'domain')
    def _compute_name(self):
        self.name = ' '.join(
            [x for x in [self.lead_source and self.lead_source.name, self.domain]
             if x])
