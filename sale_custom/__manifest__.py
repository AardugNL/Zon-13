# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################


{
    'name': "E-Mail alias on Sales order, Task and Opportunity",
    'summary': 'SO configure with alias and mail body in SO chatter',
    'version': '13.0.0.1',
    'author': 'Aardug',
    'category': 'Sale, Ptoject, CRM',
    'website': 'https://www.aardug.nl',
    'depends': ['mail','sale','opportunity_code','project_task_code','project_formulier_code'],
    'data': [
        'views/sale_view.xml',
    ],
    'auto_install': False,
    'installable': True
}
