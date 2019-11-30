# -*- coding: utf-8 -*-

import logging
from odoo import fields, http, _, SUPERUSER_ID
from odoo.addons.quotation_images_feedback.controllers.main import WebFormulier
from odoo.http import request
import json
from datetime import date

_logger = logging.getLogger(__name__)

class WebFormulierMaterial(WebFormulier):

    @http.route(['/material_update/'], type='json', auth="public", website=True)
    def update_consumed_material(self, record_id, consumed_qty, **kw):
        """ Update Consumed material id """

        if record_id:
            consumed_mt_id = request.env['consumed.material.line'].browse(int(record_id))
            try:
                res = consumed_mt_id.write({'consumed_qty': int(consumed_qty)})
            except Exception as ex:
                return False
        return True

    @http.route(['/material_add/'], type='json', auth="public", website=True)
    def add_consumed_material(self, que_id, product_id, consumed_qty, **kw):
        """ add Consumed material line """
        if que_id and product_id:
            consumed_material = request.env['consumed.material.line']
            product_id = request.env['product.product'].browse(int(product_id))
            que_id = request.env['question.formulier'].browse(int(que_id))
            sale_id = False
            task_id = False
            if que_id.consumed_material_ids:
                for consumed_line in que_id.consumed_material_ids:
                    sale_id = consumed_line.sale_id.id
                    task_id = consumed_line.task_id.id
            else:
                for sale in que_id.order_ids:
                    sale_id = sale.id
                for task in que_id.task_ids:
                    task_id = task.id
            consumed_mt_id = consumed_material.create({
                            'product_id': product_id.id,
                            'planned_qty': consumed_qty or 1,
                            'consumed_qty': int(consumed_qty),
                            'name': product_id.name,
                            'product_uom': product_id.uom_id.id,
                            'sale_id': sale_id,
                            'task_id': task_id,
                        })
            return True
        return False

    @http.route(['/question/formulier/<int:res_id>/accept'], type='json', auth="public", website=True)
    def portal_formulier_accept(self, res_id, name=None, signature=None):
        question_frm_id = request.env['question.formulier'].sudo().browse(res_id)
        question_frm_id.signature = signature
        question_frm_id.signed_by = name
        return {
            'force_refresh': True,
            'redirect_url': '/question/formulier/'+str(res_id),
        }
