# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

{
    'name': 'Project Resource Availability',
    'summary': 'Project Resource Availaility Report',
    'description': '''
        This module give the status of resource like which resource
        is free, which have schedule, on leave, available, etc..
    ''',
    'author': 'Aardug',
    'website': 'http://www.aardug.nl/',
    'support': 'info@aardug.nl',
    'category': 'Resource',
    'version': '13.0.0.1', 
    'depends': [
        'project_task_schedule',
        'project_resource_status',
        'project_resource_summary'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/template.xml',
        'views/resource_availability_view.xml',
        'wizard/task_of_day.xml'
    ],
    'js': ['static/src/js/resource_availability.js'],
    'qweb': [
        'static/src/xml/resource_availability_template.xml',
    ],
    'application': True,
}
