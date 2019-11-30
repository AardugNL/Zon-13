# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Caret IT Solutions Pvt. Ltd. (Website: www.caretit.com).           #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################
{
    'name': 'Lead Category Formulier',
    'version': '13.0.0.1',
    'summary': 'Add dropdown(Question Type) field In EC Category',
    'description': """1) Add Selection(Question Type) field In EC Category.
                      2) Question type selection field get dynamically all options from project formulier question type field.
                      3) lead fill question type field from category field.""",
    'category': 'CRM',
    'author': "Caret IT Solutions Pvt. Ltd.",
    'website': 'https://www.caretit.com',
    'depends': ['quotation_images_feedback'],
    'data': [
                'views/crm_lead_view.xml',
                'data/ir_cron_data.xml'
            ],
    'installable': True,
    'application': True,
}
