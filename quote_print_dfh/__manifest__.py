# -*- coding: utf-8 -*-

{
    'name': 'Quotation DFH Layout',
    'author': 'Aardug',
    'website': "http://www.aardug.nl",
    'category': 'Website',
    'summary': 'Add custom layout in report layout on quote template model',
    'version': '12.0',
    'description': """
                    Print quotation DFH Layout
        """,
    'depends': ['quote_print',
                'quotation_images_feedback'],
    'data': [
        'report/dfh_template.xml',
        'report/quotation_report.xml',
    ],
    'demo': [
    ],
    'installable': True,
}
