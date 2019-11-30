# -*- coding: utf-8 -*-
{
    'name': 'Quotation Image And Feedback',
    'author': 'Caret IT Solutions PVT. LTD.',
    'category': 'Website',
    'website': 'http://www.caretit.com',
    'version': '1.0',
    'summary': '',
    'description': """
    1. This module for create Question Form, This Record Create from crm_lead Record.
    2. Some Details get from crm_lead and some details fill by Customer,
    3. Form Edit from Backend and also from Website. we send link to Customer,
        So Customer can go on that page and update form,
    4. We add image feature on web form, Customer can upload images. that images show
        in website quotation page when user update any snippet image.
    5. We give new tab on edit mode of image, here so only order.image images.
    6. add lead_category module because soort field value fill-up automatic base on lead_category field
    7. add partner_salutation module for get dynamic value of salutation by custom object in online quote 
    8. add lead_source module for add many2one field on user form, this field use in another modules like online_opportunity_form
    """,
    'depends': ['website_crm','quote_print','sale_timesheet','lead_category','partner_salutation','lead_source'],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_order_view.xml',
        'views/crm_lead_view.xml',
        'views/project_formulier_view.xml',
        'views/res_users_view.xml',
        'views/access_assets.xml',
        'views/tabs_template.xml',
        'views/formulier_profile_template.xml',
        'views/formulier_media_template.xml',
        'views/first_question_form.xml',
        'views/second_question_form.xml',
        'views/third_question_form.xml',
        'views/formulier_template.xml',
        'views/website_template.xml',
        'views/snippets.xml',
    ],
    'qweb': [
        'static/src/xml/wysiwyg.xml',
        ],
    'installable': True,
}
