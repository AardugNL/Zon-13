# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Caret IT Solutions Pvt. Ltd. (Website: www.caretit.com).           #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################
{
    'name': 'Opportunity Name',
    'version': '13.0.1.0',
    'summary': 'Crm Lead',
    'description': """When Convert Lead To Opportunity Then Customer name, city, street Fields 
                      Merge in Name Field""",
    'category': 'CRM',
    'author': "Caret IT Solutions Pvt. Ltd.",
    'website': 'https://www.caretit.com',
    'depends': ['crm','base_address_extended','lead_category'],
    'data': [
            'views/crm_lead_view.xml',
            ],
    'installable': True,
    'application': True,
}
