# -*- coding: utf-8 -*-

{
    'name': 'Formulier Three',
    'version': '13.0.4.0',
    'summary': '',
    'description': """ """,
    'category': 'CRM',
    'author': "Caret IT Soltions PVT. LTD.",
    'website': "http://caretit.com",
    'depends': ['quotation_images_feedback', 'ec_watt_piek_iso','sale_margin'],
    'data': [
            'security/ir.model.access.csv',
            'data/data.xml',
            'views/access_assets.xml',
            'views/res_user_view.xml',
            'views/formulier_config_settings_view.xml',
            'views/product_view.xml',
            'views/formulier_view.xml',
            'views/sale_order_view.xml',
            'views/first_question_form.xml',
            'views/second_question_form.xml',
            'views/third_question_form.xml',
            'views/quote_configuration_form.xml',
            'views/tabs_template.xml',
            ],
    'installable': True,
    'application': True,
}
