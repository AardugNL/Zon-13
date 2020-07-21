# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

{
    'name': 'Project Resource Summary',
    'summary': 'Summary of Project Resource',
    'description': '''
        This module give the summary details like which resource on leave which has schedule 
        betweek selected date and also display task between selected date.
    ''',
    'author': 'Aardug',
    'website': 'http://www.aardug.nl/',
    'support': 'info@aardug.nl',
    'category': 'Resource',
    'version': '13.0.0.1',
    'depends': ['project_task_schedule'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/summary.xml',
    ],
    'application': True,
}
