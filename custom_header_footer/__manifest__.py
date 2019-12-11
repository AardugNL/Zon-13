# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Caret IT Solutions Pvt. Ltd. (Website: www.caretit.com).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

{
    'name': 'Custom Header Footer',
    'version': '13.0',
    'category': 'Reports',
    'author': 'Caret IT Solutions Pvt. Ltd.',
    'website': 'http://www.caretit.com/',
    'description': """
        Change Header/Footer content in reports of sale,invoice,stock records,
        Based on Dropdown Tradmark(company) selection.
        Add Dropdown field with 4 options on Model sale,invoice and stock.
        Add 4 different images for header of report and add also for same footer.
    """,
    'depends': ['crm', 'sale', 'sale_crm', 'account', 'stock'],
    'data': [
            'data/paperformate_data.xml',
            'views/view_res_company.xml',
            'views/view_models.xml',
            'report/ec_layout.xml',
            'report/sale_invoice_reports.xml',
        ],
    'installable': True,
    'application': False,
}
