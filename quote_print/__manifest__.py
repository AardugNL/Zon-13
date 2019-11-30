# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

{
    'name': 'Print Quotation',
    'author': 'Aardug, Arjan Rosman',
    'category': 'Sale',
    'summary': 'Extend Functionality of Sale online quatation',
    'website': 'http://www.aardug.nl/',
    'support': 'arosman@aardug.nl',
    'version': '13.0.1.0',
    'description': '',
    'depends': ['sale_management',
                'sale_quotation_builder',
                'custom_header_footer',
                'website_sale',
                'sale'],
    'data': [
        'data/quote_custom_header.xml',
        'data/mail_template_data.xml',
        'data/partnership_contact_template.xml',
        'views/quote_print.xml',
        'views/res_users_view.xml',
        'views/snippets.xml',
        'views/quote_template.xml',
        'views/online_so_template.xml',
        'report/external_header_footer.xml',
        'report/quotation_report_first_page.xml',
        'report/quotation_report.xml',
        'report/sale_order_reports.xml',
        'report/cover_image_report.xml',
        'report/close_image_report.xml',
    ],
    'demo': [
    ],
    'qweb': ['static/src/xml/hide_translation_msg.xml'],
    'installable': True,
}
