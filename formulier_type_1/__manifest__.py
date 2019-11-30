# -*- coding: utf-8 -*-

{
    'name': 'Formulier one',
    'version': '13.0.1.0',
    'summary': '',
    'description': """ """,
    'category': 'CRM',
    'author': "Caret IT Soltions PVT. LTD.",
    'website': "http://caretit.com",
    'depends': ['quotation_images_feedback'], #quote_print
    'data': [
            'security/ir.model.access.csv',
            'data/data.xml',
            'views/access_assets.xml',
            'views/formulier_view.xml',
            'views/first_question_form.xml',
            'views/second_question_form.xml',
            'views/third_question_form.xml',
            'views/snippets.xml',
            ],
    'installable': True,
    'application': True,
}
