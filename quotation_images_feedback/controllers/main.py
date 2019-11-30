# -*- coding: utf-8 -*-

import logging
from odoo import fields, http, _, SUPERUSER_ID
from odoo.http import request
import json
import base64

_logger = logging.getLogger(__name__)

class WebFormulier(http.Controller):

    @http.route(['/web/video/<int:video_id>'], type='http', auth="user", website=True)
    def video_url(self, video_id, **kw):
        """ video binary data return """

        if video_id:
            order_video = request.env['order.video'].browse(video_id)
            video = base64.b64decode(order_video.video)
            return video
        return False

    @http.route(['/country_infos/<int:country_id>'], type='json', auth="user", website=True)
    def get_state_id(self, country_id, **kw):
        """ State show on Web Form """

        state_ids = request.env['res.country.state'].search_read(
            [('country_id','=',country_id)],['name'])
        return state_ids

    @http.route(['/question/formulier/submit/<int:question_frm_id>/<string:model_name>'], type='http',
                auth='user', methods=['POST'], website=True)
    def question_formulier_submit(self,question_frm_id,model_name, **kwargs):
        """ Project Formulier web form submit """
        if question_frm_id:
            if kwargs.get('product_id'):
                kwargs.pop('product_id')
            if kwargs.get('product_qty'):
                kwargs.pop('product_qty')
            if kwargs.get('state_id'):
                kwargs.pop('state_id')
            if kwargs.get('country_id'):
                kwargs.pop('country_id')
            if kwargs.get('que_id'):
                kwargs.pop('que_id')
            question_frm_id = request.env['question.formulier'].sudo().browse(question_frm_id)
            if question_frm_id.state == 'opportunity':
                question_frm_id.state = 'opportunity_output'
            elif question_frm_id.state == 'quotation':
                question_frm_id.state = 'quotation_output'
            elif question_frm_id.state == 'task':
                question_frm_id.state = 'task_output'
            if kwargs.get('question_image_upload_input[0]'):
                del kwargs['question_image_upload_input[0]']
            if kwargs.get('question_video_upload_input[0]'):
                del kwargs['question_video_upload_input[0]']
            if kwargs.get('question_document_upload_input[0]'):
                del kwargs['question_document_upload_input[0]']
            question_frm_id.write(kwargs)
            return json.dumps({'id': question_frm_id.id})

    @http.route(['/question/formulier/<int:question_frm_id>'], type='http', auth="user", website=True)
    def question_formulier_page(self, question_frm_id, **kw):
        """ Project Formulier view on web form """

        question_frm_id = request.env['question.formulier'].sudo().browse(question_frm_id)
        user = request.env.user
        if question_frm_id and question_frm_id.partner_id:
            if user.has_group('base.group_user') or user.partner_id.id == question_frm_id.partner_id.id:
                values = question_frm_id.sudo().online_pf_dictionary()
                return request.render('quotation_images_feedback.question_formulier_template', values)
            else:
                return request.redirect('/my')
        else:
            return request.redirect('/my')

    @http.route('/question/form/image/upload',auth="user", website=True, type="json", csrf=False)
    def question_form_image_upload_file(self, image, fileName, file_type, que_id, is_task):
        """ Project Formulier web form -> extra images directly create new record """

        OrderImage = request.env['order.image'].create({
                                                    'name': fileName,
                                                    'image': image,
                                                    'file_type': file_type or 'application/png',
                                                    'question_frm_id': int(que_id),
                                                    'is_task': is_task,
                                                    })
        return OrderImage.id

    @http.route('/question/form/video/upload',auth="user", website=True, type="json", csrf=False)
    def question_form_video_upload_file(self, video, fileName, file_type, que_id, is_task):
        """ Project Formulier web form -> extra videos directly create new record """
        OrderVideo = request.env['order.video'].create({
                                                    'name': fileName,
                                                    'video': video,
                                                    'file_type': file_type or 'application/mp4',
                                                    'question_frm_id': int(que_id),
                                                    'is_task': is_task,
                                                    })
        return OrderVideo.id

    @http.route('/question/form/document/upload',auth="user", website=True, type="json", csrf=False)
    def question_form_document_upload_file(self, document, fileName, file_type, que_id):
        """ Project Formulier web form -> extra document directly create new record """
        OrderDocument = request.env['order.document'].create({
                                                    'name': fileName,
                                                    'file': document,
                                                    'file_type': file_type or 'application/pdf',
                                                    'question_frm_id': int(que_id),
                                                    })
        return OrderDocument.id,OrderDocument.name

    @http.route(['/sale_order/project_formulier/get'], type='json', auth="public", website=True)
    def get_images(self, order_id, res_model, **kw):
        """ quotation image tab on quotation preview""" 

        data = {'formulier_id': '', 'data':[], 'image_ids':[], 'document_ids': [], 'video_ids': []}
        if res_model == 'sale.order':
            order_id = request.env['sale.order'].browse(order_id)
            if order_id and order_id.question_frm_id:
                que_id = order_id.question_frm_id
                data.update({'formulier_id': que_id.id, 'data':[]})
                if que_id.image_ids:
                    data['image_ids'].append(que_id.image_ids.ids)
                for doc in que_id.document_ids:
                    data['document_ids'].append([doc.id, doc.name])
                for video in que_id.video_ids:
                    data['video_ids'].append([video.id, video.name])
                formulerModelId = request.env['ir.model'].search([('model', '=', 'question.formulier')])
                fields = request.env['ir.model.fields'].search([('ttype', '=', 'binary'),
                    ('model_id', '=', formulerModelId.id)])
                for field in fields:
                    imageData = request.env['question.formulier'].search_read(
                        [('id', '=', que_id.id)], [field.name])
                    if imageData[0].get(field.name):
                        data['data'].append(field.name)
        if res_model == 'sale.order.template':
            template_id = request.env['sale.order.template'].browse(order_id)
            if template_id:
                for video in template_id.template_video_ids:
                    data['video_ids'].append([video.id, video.name])
        return data
