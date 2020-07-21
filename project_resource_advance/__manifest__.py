# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

{
    'name': 'Project Resource Advance',
    'summary': 'Manage Project Resource in Advanced',
    'description': '''
        This module extends user experience for managing resources effectivel.
    ''',
    'author': 'Aardug',
    'website': 'http://www.aardug.nl/',
    'support': 'info@aardug.nl',
    'category': 'Resource',
    'version': '13.0.0.1',
    'depends': ['project_task_schedule',
                'project_resource_status'],
    'data': [
        'data/project_task_cron.xml',
        'views/project_task_view.xml',
        'wizard/resource_wizard.xml'
    ],
}
