# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

{
    'name': 'Task Billing Restriction',
    'summary': ('Only \'Billing Administrator\' or higher authority can only move '
                'task to specific stage.'),
    'description': '',
    'author': 'Aardug',
    'website': 'http://www.aardug.nl/',
    'support': 'info@aardug.nl',
    'category': 'Resource',
    'version': '13.0.0.1',
    'depends': ['project', 'account'], 
    'data': [
        'views/view.xml',
    ],
    'application': True,
}
