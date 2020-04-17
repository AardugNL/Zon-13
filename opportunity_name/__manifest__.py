# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

{
    'name': 'Opportunity Name',
    'version': '13.0.1.0',
    'summary': 'Crm Lead',
    'description': """When Convert Lead To Opportunity Then Customer name, city, street Fields 
                      Merge in Name Field""",
    'category': 'CRM',
    'author': "Aardug",
    'website': 'https://www.aardug.nl',
    'depends': ['crm','base_address_extended','lead_category'],
    'data': [
            'views/crm_lead_view.xml',
            ],
    'installable': True,
    'application': True,
}
