# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Caret IT Solutions Pvt. Ltd. (Website: www.caretit.com).           # 
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

{
    'name' : 'white label description',
    'version': '13.0.1.0',
    'summary': 'show white label description and White label sales price.',
    'category': 'products',
    'description': """ This Module Allowes to you set two different 
    price and description for product and also allow you to set product box on 
    sale order line and on product form""",
    'author': 'Caret IT Solutions Pvt. Ltd.',
    'website': 'http://www.caretit.com',
    'depends': ['base','product', 'sale_management', 'purchase', 
    'sale', 'sale_crm', 'base_address_extended', 'stock'],
    'data': [
             'views/product_view.xml',
             'views/sale_view.xml',
             'views/account_move_views.xml',
             'views/res_partner_view.xml',
             'views/purchase_view.xml',
            ],
    'qweb': [
            'static/src/xml/box_at_date.xml',
            'static/src/xml/purchase_box_at_date.xml'
            ],
    'installable': True,
    'application': True,
}
