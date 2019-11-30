# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Caret IT Solutions Pvt. Ltd. (Website: www.caretit.com).           #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################
{
    'name': 'EC Watt Piek and EC ISO',
    'version': '13.0.1.0',
    'summary': 'Add EC Watt Piek and EC ISO in product and EC Order Watt Piek, EC Order ISO in Sale and Analysis Pivot',
    'description': """EC Watt Piek and EC ISO in product and EC Order Watt Piek, EC Order ISO in Sale and Analysis Pivot""",
    'category': 'CRM',
    'author': "Caret IT Solutions Pvt. Ltd.",
    'website': 'https://www.caretit.com',
    'depends': ['sale'],
    'data': [
            'views/product_sale.xml',
            ],
    'installable': True,
    'application': True,
}
