# -*- coding: utf-8 -*-

import logging
from odoo import fields, http, _, SUPERUSER_ID
from odoo.http import request
from odoo.addons.quotation_images_feedback.controllers.main import WebFormulier
import json
import base64

_logger = logging.getLogger(__name__)

class WebFormulier(WebFormulier):

    @http.route(['/question/formulier/submit/<int:question_frm_id>/<string:model_name>'], type='http',
                auth='user', methods=['POST'], website=True)
    def question_formulier_submit(self,question_frm_id,model_name, **kwargs):
        """ Project Formulier web form submit """
        if question_frm_id:
            question_frm_id = request.env['question.formulier'].browse(question_frm_id)
            if kwargs.get('foundation_name'):
                for foundation_img in question_frm_id.foundation_construction_ids:
                    if foundation_img.id == int(kwargs.get('foundation_name')):
                        foundation_img.is_selected = True
                    else:
                        foundation_img.is_selected = False
                del kwargs['foundation_name']
            question_frm_id = question_frm_id.id

        return super(WebFormulier, self).question_formulier_submit(question_frm_id,model_name,**kwargs)

    @http.route(['/order/record'], type='json', auth="public", website=True, csrf=False)
    def get_sale(self, sale_id):
        order = request.env['sale.order'].browse(sale_id)
        if order and order.question_frm_id:
            my_dict = {}
            if order.question_frm_id.customer_type == 'formulier_one':
                for foundation_construction_id in order.question_frm_id.foundation_construction_ids:
                    if foundation_construction_id.is_selected == True:
                        my_dict['foundation_construction_name'] = foundation_construction_id.name
                        my_dict['foundation_construction_image']= foundation_construction_id.image
                return {'question_frm_id': order.question_frm_id.id,
                        'quotation_template_id': order.sale_order_template_id and order.sale_order_template_id.id,
                        # 'pdf_name': order.sale_order_template_id and order.sale_order_template_id.file_name_pdf,
                        'image': order.question_frm_id.image or False,
                        'plattegrond_img': order.question_frm_id.plattegrond_img or False,
                        'fundering_img': order.question_frm_id.fundering_img or False,
                        'blueprint_img': order.question_frm_id.blueprint_img or False,
                        'lot_img': order.question_frm_id.lot_img or False,
                        'extra_drawing_1_img': order.question_frm_id.extra_drawing_1_img or False,
                        'extra_drawing_2_img': order.question_frm_id.extra_drawing_2_img or False,
                        'image_1': order.question_frm_id.image_1 or False,
                        'image_2': order.question_frm_id.image_2 or False,
                        'image_3': order.question_frm_id.image_3 or False,
                        'image_4': order.question_frm_id.image_4 or False,
                        'image_5': order.question_frm_id.image_5 or False,
                        'image_6': order.question_frm_id.image_6 or False,
                        'image_7': order.question_frm_id.image_7 or False,
                        'image_8': order.question_frm_id.image_8 or False,
                        'house_info': order.question_frm_id.house_info,
                        'analysis_settlement': order.question_frm_id.analysis_settlement,
                        'floor_construction': order.question_frm_id.floor_construction or '',
                        'leads': order.question_frm_id.leads or '',
                        'goal_owner': order.question_frm_id.goal_owner,
                        'faced_construction': order.question_frm_id.faced_construction or '',
                        'floor_construction_verd': order.question_frm_id.floor_construction_verd or '',
                        'inspection_foundation_depth': order.question_frm_id.inspection_foundation_depth,
                        'possible_settings': order.question_frm_id.possible_settings,
                        'action_resident': order.question_frm_id.action_resident,
                        'location_pipping_ground': order.question_frm_id.location_pipping_ground,
                        'action_total_wall': order.question_frm_id.action_total_wall,
                        'parkeren': order.question_frm_id.parkeren,
                        'toegang': order.question_frm_id.toegang,
                        'tuin': order.question_frm_id.tuin,
                        'bomen': order.question_frm_id.bomen,
                        'kraan': order.question_frm_id.kraan,
                        'grondwerk': order.question_frm_id.grondwerk,
                        'aanvullend': order.question_frm_id.aanvullend,
                        'quot_name': order.question_frm_id.lead_id.user_id.name or 'Dhr Ferry Nieuwboer',
                        'customer_city': order.question_frm_id.partner_id.city,
                        'customer_street': order.question_frm_id.partner_id.street,
                        'quote_date': order.question_frm_id.date_opportunity,
                        'faced_construction': order.question_frm_id.faced_construction or '',
                        'floor_construction_verd_2': order.question_frm_id.floor_construction_verd_2 or '',
                        'dakbouw': order.question_frm_id.dakbouw or '',
                        'quote_soort': order.question_frm_id.lead_id.soort,
                        'foundation_construction_name': my_dict.get("foundation_construction_name"),
                        'foundation_construction_image': my_dict.get("foundation_construction_image"),
                    }
            else:
                return {'question_frm_id': False,}
        else:
            return {'question_frm_id': False,}
