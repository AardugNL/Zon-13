# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

{
    'name': 'Project Task Resource Kanban',
    'summary': 'Project Task Resource Management',
    'description': '''
        This module give user experince to manage task and resource form one
        kanban view.
        Functionality:
        1. drag & drop task and resources
        2. create schedule on drag & drop
    ''',
    'author': 'Aardug',
    'website': 'http://www.aardug.nl/',
    'support': 'info@aardug.nl',
    'category': 'Resource',
    'version': '13.0.0.1',
    'depends': ['project_task_schedule'],
    'data': [
        'security/ir.model.access.csv',
        'data/task_resource_cron.xml',
        'views/task_resource_view.xml',
        'views/templates.xml',
    ],
    'application': True,
}
