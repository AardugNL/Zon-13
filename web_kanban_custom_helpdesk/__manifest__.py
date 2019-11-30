# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

{
    'name': 'Web Kanban Custom Help Desk',
    'description': """
    Extensive kanban view for managing business flow of Help Desk system.
    """,
    'version': '1.0',
    'category': 'Custom',
    'author': "Aardug, Arjan Rosman",
    'website': "http://www.aardug.nl/",
    'support': 'arosman@aardug.nl',
    'depends': ['helpdesk'],
    'data': [
        'data/helpdesk_action_rule_data.xml',
        'security/ir.model.access.csv',
        'views/web_kanban_custom.xml',
        'views/helpdesk_view.xml',
    ],
    'application': False,
    'installable': True,
    'auto_install': False,
}
