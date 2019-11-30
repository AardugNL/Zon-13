# -*- coding: utf-8 -*-
##############################################################################
#
#
##############################################################################

{
    'name': 'Opportunity Meeting',
    'version': '13.0.0.1',
    'description': """
        This module usage is Create a calendar meeting to sync with Google.
    """,
    'summary': 'Create a Opportunity Meeting For Calendar.',
    'category': 'CRM',
    'author': "Aardug",
    'website': "http://www.aardug.nl",
    'depends': ['crm', 'crm_sales_person_report'],
    'data': ['data/stage_and_activity_demo.xml',
             'views/crm_meeting_view.xml'],
    'test': [],
    'installable': True,
    'auto_install': False,
}
