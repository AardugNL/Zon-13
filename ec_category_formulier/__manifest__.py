# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

{
    'name': 'Lead Category Formulier',
    'version': '13.0.0.1',
    'summary': 'Add dropdown(Question Type) field In EC Category',
    'description': """1) Add Selection(Question Type) field In EC Category.
                      2) Question type selection field get dynamically all options from project formulier question type field.
                      3) lead fill question type field from category field.""",
    'category': 'CRM',
    'author': "Aardug",
    'website': 'https://www.aardug.nl',
    'depends': ['quotation_images_feedback'],
    'data': [
                'views/crm_lead_view.xml',
                'data/ir_cron_data.xml'
            ],
    'installable': True,
    'application': True,
}
