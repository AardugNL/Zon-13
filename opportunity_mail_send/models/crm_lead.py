from odoo import models, fields, api, tools

class OpportunityMail(models.Model):

    _name = "opportunity.mail.configure"
    _description = "Configure for mail send on convert lead to opportunity"

    name = fields.Char(string="Name")
    lead_lead_source = fields.Many2one("lead.source", string="Ec Lead Source")
    lead_category = fields.Many2one("lead.category", string="Lead Category")
    email_template_id = fields.Many2one("mail.template", string="Email Template")
    zip_range_from = fields.Integer(string="Zip code range from")
    zip_range_to = fields.Integer(string="Zip code range to")

class CrmLead(models.Model):
    _inherit = "crm.lead"

    def _convert_opportunity_data(self, customer, team_id=False):
        res = super(CrmLead,self)._convert_opportunity_data(customer, team_id)
        OpportunityConfig = self.env['opportunity.mail.configure']
        if self.lead_lead_source and self.lead_category and self.partner_id and len(self.zip) > 1:
            opportunity_config = OpportunityConfig.search([('lead_lead_source', '=', self.lead_lead_source.id),
                                        ('lead_category', '=', self.lead_category.id),
                                        ('zip_range_from', '<=', int(self.zip[0:2])),
                                        ('zip_range_to', '>=', int(self.zip[0:2])),], limit=1)
            if opportunity_config and opportunity_config.email_template_id:
                template_id = opportunity_config.email_template_id
                template_id.send_mail(self.id, force_send=True)
        return res
