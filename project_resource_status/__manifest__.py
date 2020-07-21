# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

{
    'name': 'Project Resource Status',
    'summary': 'Project Resource Daily Status',
    'description': '''
        This module give the summary details like which resource on leave
        which has schedule between selected date and also display task between
        selected date.
    ''',
    'author': 'Aardug',
    'website': 'http://www.aardug.nl/',
    'support': 'info@aardug.nl',
    'category': 'Resource',
    'version': '13.0.0.1',
    'depends': ['project_task_schedule', 'hr_holidays'],
    'data': [
        'security/ir.model.access.csv',
        'data/resource_cron.xml',
        'views/resource_status.xml',
        'wizard/resource_status_wizard.xml',
        'data/resource_status.xml'
    ],
}
