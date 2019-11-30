# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Caret IT Solutions Pvt. Ltd. (Website: www.caretit.com).           #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################
{
    'name': 'Mail send on convert lead to opportunity',
    'version': '13.0.1.0',
    'summary': '',
    'description': """Send different Mail format(template) to customer on Convert lead to opportunity.
                    Add fields like lead source, lead category, email template and zip range in new model (opportunity.mail.configure),
                    Based on some comparision of fields, get email template from model(opportunity.mail.configure) and using that template mail send to customer""",
    'category': 'CRM',
    'author': "Caret IT Solutions Pvt. Ltd.",
    'website': 'https://www.caretit.com',
    'depends': ['lead_source', 'lead_category'],
    'data': [
            'security/ir.model.access.csv',
            'views/crm_lead_view.xml',
            ],
    'installable': True,
    'application': True,
}
