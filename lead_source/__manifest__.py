# -*- coding: utf-8 -*-
##############################################################################
##############################################################################
{
    'name': 'Lead Source',
    'version': '13.0.1.0',
    'sequence': 4,
    'summary': 'Add Lead Source to Crm Lead',
    'description': """Add Lead Source to Crm Lead and Pivot Reports""",
    'category': 'CRM',
    'author': "Aardug, Arjan Rosman",
    'website': "http://www.aardug.nl/",
    'support': 'arosman@aardug.nl',
    'depends': ['sale', 'crm', 'sale_crm'],
    'data': [
            'security/ir.model.access.csv',
            'views/crm_lead_view.xml',
            ],
    'installable': True,
    'application': True,
}
