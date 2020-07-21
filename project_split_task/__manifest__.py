# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

{
    'name': 'Split Project Task',
    'summary': 'Split Project Task',
    'description': '''
        This module split the tasks if date start and date end difference is
        more than one days.
        2 butttons display "spit task" and "split task 2"
        "split task" button create tasks for all days between dates,
        and "split task 2" button create tasks for working days only.
    ''',
    'author': 'Aardug',
    'website': 'http://www.aardug.nl/',
    'support': 'info@aardug.nl',
    'category': 'Resource',
    'version': '13.0.0.1',
    'depends': ['project_task_schedule'],
    'data': [
        'views/split_task.xml',
    ],
    'application': True,
}
