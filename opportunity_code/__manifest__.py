# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################


{
    'name': 'Sequential Code for Opportunity',
    'version': '13.0.0.1',
    'category': 'crm lead',
    'author': 'Aardug',
    'website': 'https://www.aardug.nl',
    'depends': ['crm'],
    'data': [
        'data/opportunity_sequence.xml',
        'views/opportunity_view.xml',
    ],
    'installable': True,
    "pre_init_hook": "create_code_equal_to_id",
    "post_init_hook": "assign_old_sequences",
}
