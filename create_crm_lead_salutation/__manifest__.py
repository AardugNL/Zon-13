# -*- coding: utf-8 -*-

{
    'name': 'Fill Salutation from email template',
    'version': '13.0.0.1',
    'category': 'CRM',
    'sequence': 1,
    'summary': '',
    'description': """
This module inherit create_crm_lead module and make automatic fill-up fields value of salutation module when lead create from email template
""",
    'author': "Caret IT Soltions PVT. LTD.",
    'website': "http://caretit.com",
    'depends': [
        'create_crm_lead', 'partner_salutation',
    ],
    'data': [],
    'demo': [],
    'test': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': [],
}
