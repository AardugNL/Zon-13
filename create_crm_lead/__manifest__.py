# -*- coding: utf-8 -*-

{
    'name': 'Base Module for Email Templates',
    'version': '13.0.0.1',
    'category': 'CRM',
    'sequence': 1,
    'summary': '',
    'description': """
This module enables automatic lead creation in v11 community from fetched email\'s body content using the server action
(created by this module).This server action need to be used in fetchmail configuration to enable automatic lead creation
from the body content.This module also sends an email to the generated lead's email address if there is any active outgoing 
email server configured,otherwise, it will have those emails in exception state under 'Setting/Technical/Email/Emails', 
which then can be send manually when any outgoing email server is configured.
""",
    'author': "Aardug, Arjan Rosman",
    'website': "http://www.aardug.nl/",
    'support': 'arosman@aardug.nl',
    'depends': [
        'crm', 'mail', 'lead_category', 'lead_source', 'sales_team', 'mail_add_action'
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/crm_action_rule_data.xml',
        'views/crm_lead_tree_view.xml'
    ],
    'demo': [],
    'test': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': [],
}
