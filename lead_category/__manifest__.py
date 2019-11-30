# -*- coding: utf-8 -*-
##############################################################################
##############################################################################
{
    'name': 'Lead Category',
    'version': '13.0.1.0',
    'sequence': 4,
    'summary': 'Add Lead Category to Crm Lead',
    'description': """Add Lead Category to Crm Lead and Pivot Reports""",
    'category': 'CRM',
    'author': "Aardug, Arjan Rosman",
    'website': "http://www.aardug.nl/",
    'support': 'arosman@aardug.nl',
    'depends': ['lead_source','sale','crm','sale_crm'],
    'data': [
            'security/ir.model.access.csv',
            'data/lead_category_data.xml',
            'views/crm_lead_view.xml',
            ],
    'installable': True,
    'application': True,
}
