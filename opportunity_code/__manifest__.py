# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Caret IT Solutions Pvt. Ltd. (Website: www.caretit.com).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

{
    'name': 'Sequential Code for Opportunity',
    'version': '13.0.0.1',
    'category': 'crm lead',
    'author': 'Caret It Solutions PVT. LTD.',
    'website': 'https://caretit.com',
    'depends': ['crm'],
    'data': [
        'data/opportunity_sequence.xml',
        'views/opportunity_view.xml',
    ],
    'installable': True,
    "pre_init_hook": "create_code_equal_to_id",
    "post_init_hook": "assign_old_sequences",
}
