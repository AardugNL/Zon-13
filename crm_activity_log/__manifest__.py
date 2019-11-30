# -*- coding: utf-8 -*-
##############################################################################
#
#
##############################################################################

{
    'name': 'CRM Activity Log',
    'version': '13.0.0.1',
    'summary': 'CRM Activity Log when stage change',
    'description': """New Record Created To Save Opporunity History.""",
    'category': 'CRM',
    'author': "Aardug, Arjan Rosman",
    'website': "http://www.aardug.nl/",
    'depends': ['crm'],
    'data': [
            'security/ir.model.access.csv',
            'views/activity_log_view.xml',
            ],
}
