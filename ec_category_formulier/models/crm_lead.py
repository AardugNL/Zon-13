from odoo import api, fields, models, _

class QuestionTypeToEcCategory(models.Model):
    _inherit = "lead.category"

    customer_type = fields.Selection('_get_selection', string="Question Type", store=True)

    @api.model
    def _get_selection(self):
        """ dynamically get all selection field options"""
        cus_type = []
        CRM = self.env['crm.lead']
        if 'customer_type' in CRM._fields.keys():
            cus_type = self.env['crm.lead'].fields_get('customer_type')['customer_type']['selection']
        return cus_type

class UpdateCrmLead(models.Model):
    _inherit = "crm.lead"

    @api.onchange('lead_category')
    def onchange_customer_type(self):
        """ use try catch beacuse if lead have not same customer type selection field options then it not give error"""
        try:
            self.customer_type = self.lead_category.customer_type
        except Exception as e:
            pass

    @api.model
    def create(self, vals):
        res = super(UpdateCrmLead, self).create(vals)
        if not vals.get('customer_type'):
            if vals.get('lead_category'):
                try:
                    res.customer_type = self.env['lead.category'].browse(vals['lead_category']).customer_type
                except Exception as e:
                    pass
        return res

    def write(self, vals):
        res = super(UpdateCrmLead, self).write(vals)
        if vals.get('lead_category') and not self.customer_type:
            try:
                self.customer_type = self.env['lead.category'].browse(vals['lead_category']).customer_type
            except Exception as e:
                pass
        return res