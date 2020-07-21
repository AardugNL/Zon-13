# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

{
    'name': 'Project Task Schedule',
    'summary': 'Schedule on Tasks for resources.',
    'description': '''
        1. Create schedules for task
        2. Reschedule task
        3. create timesheet auto for schedules
        4. create metting for schedule
    ''',
    'author': 'Aardug',
    'website': 'http://www.aardug.nl/',
    'support': 'info@aardug.nl',
    'category': 'Project',
    'version': '13.0.1.0',
    'depends': ['project_resource', 'hr_timesheet'],
    'data': [
        'security/ir.model.access.csv',
        'data/schedule_cron.xml',
        'views/task_schedule.xml',
        'views/project_task.xml'
    ],
}
