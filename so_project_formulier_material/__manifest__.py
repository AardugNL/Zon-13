# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################


{
    'name': 'SO Project Formulier Material',
    'author': 'Aardug',
    'website': 'http://www.aardug.nl',
    'category': 'Project',
    'summary': '',
    'version': '13.0.0.1',
    'description': """
        This module aims to syncronise sale order task material with project task material.
        """,
    'depends': ['so_project_task_material','quotation_images_feedback'],
    'data': [
        'security/ir.model.access.csv',
        'views/access_assets.xml',
        'views/task_view.xml',
        'views/task_material_form.xml',
        'views/customer_questions.xml',
    ],
    'installable': True,
}
