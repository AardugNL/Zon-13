# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

{
    'name': 'Resource Available Kanban',
    'summary': 'Display Available Resources on kanban',
    'description': '''
        This module give kanban view that display available resources and resource on leave.
    ''',
    'author': 'Aardug',
    'website': 'http://www.aardug.nl/',
    'support': 'info@aardug.nl',
    'category': 'Resource', 
    'version': '13.0.0.1',
    'depends': ['project_resource_status'],
    'data': [
        'data/available_cron.xml',
        'views/kanban_view.xml',
        'views/templates.xml'

    ],
    'application': True,
}
