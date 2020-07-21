# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

{
    'name': 'Project Resource',
    'summary': 'Project Resource Management',
    'description': '''
        This module extends user experience for managing resources effectively.
    ''',
    'author': 'Aardug',
    'website': 'http://www.aardug.nl/',
    'support': 'info@aardug.nl',
    'category': 'Resource',
    'version': '13.0.0.1',
    'depends': ['project', 'hr', 'calendar'],
    'data': [
        'security/ir.model.access.csv',
        'views/resource_view.xml',
        'views/project_task_view.xml',
    ],
}
