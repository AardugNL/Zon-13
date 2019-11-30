# -*- coding: utf-8 -*-
##############################################################################
#
#
##############################################################################

{
    'name': 'Opportunity Project Formulier Show in Meeting',
    'version': '13.0.0.1',
    'description': """
        This module usage is add 2 button on calendar meeting for direct on project formulier form view and online form view.
    """,
    'summary': 'Opportunity project formulier visible in Calendar.',
    'category': 'CRM',
    'author': "Aardug",
    'website': "http://www.aardug.nl",
    'depends': ['formulier_type_1', 'opportunity_meeting','sale_custom'],
    'data': [
        'views/crm_meeting_view.xml'
    ],
    'installable': True,
    'auto_install': False,
}
