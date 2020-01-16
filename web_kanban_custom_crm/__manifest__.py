# -*- coding: utf-8 -*-

{
    'name': 'Web Kanban Custom CRM',
    'category': 'CRM',
    'description': """
        To support CRM Opportunity kanban.
        1) user can set server actin and custom action on crm stage configuration.
        2) server action is very helpfull to do any action on opportunity like autometically stage.
        3) custom action is to set activity on opportunity autometically.
    """,
    'version': '13.0.1.1',
    'depends':['crm'],
    'author': "Caret IT Soltions PVT. LTD.",
    'website': "http://caretit.com",
    'data' : [
        'data/crm_action_rule_data.xml',
        # 'data/crm_security.xml',
        'views/web_kanban_custom.xml',
        'views/crm_view.xml',
        'security/ir.model.access.csv'
    ],
    'auto_install': False,
    'instalable': True,
}
