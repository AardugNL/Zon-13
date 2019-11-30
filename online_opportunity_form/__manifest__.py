# -*- coding: utf-8 -*-
{
    'name': 'Online Opportunity Form',
    'author': 'Caret IT Solutions PVT. LTD.',
    'category': 'Website',
    'website': 'http://www.caretit.com',
    'version': '13.0.0.0.1',
    'summary': '',
    'description': """
    1. This module for create opportunity from online form.
    """,
    'depends': ['quotation_images_feedback','lead_category','partner_salutation'],
    'data': [
        'data/crm_stage_data.xml',
        'views/access_assets.xml',
        'views/opportunity_template.xml'
    ],
    'qweb': [],
    'installable': True,
}
