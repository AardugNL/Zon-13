# -*- coding: utf-8 -*-

{
    'name': 'Web Kanban Custom Project',
    'category': 'Hidden',
    'description': """
To support Project Task/Issue kanban.

        """,
    'version': '1.0',
    'depends': ['project'],
    'author': "Aardug, Arjan Rosman",
    'website': "http://www.aardug.nl/",
    'support': 'arosman@aardug.nl',
    'data': [
        'views/web_kanban_custom.xml',
        'views/project_view.xml',
        'data/project_action_rule_data.xml',
        'data/project_action_rule_data_user.xml',
        'security/ir.model.access.csv'
    ],
    'auto_install': False,
    'installable': True,
}
