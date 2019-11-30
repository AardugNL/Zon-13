# -*- coding: utf-8 -*-

import logging
from odoo import fields, http, _
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
import json

_logger = logging.getLogger(__name__)

class FormulierPortal(CustomerPortal):
    """ overwrite protal and show user Project Formulier """

    def _prepare_portal_layout_values(self):
        values = super(FormulierPortal, self)._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        admin_partner = request.env['res.users'].sudo().browse(2).partner_id
        if admin_partner.id == partner.id:
            domain = []
        else:
            domain = [('partner_id','=',partner.id)]
        values['question_formulier_count'] = request.env['question.formulier'].search_count(domain)
        return values

    @http.route(['/my/formulier'], type='http', auth="user", website=True)
    def portal_my_formulier(self, page=1, date_begin=None, date_end=None, sortby=None,filterby=None, **kw):
        values = self._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        QuestionFormulier = request.env['question.formulier']
        admin_partner = request.env['res.users'].sudo().browse(2).partner_id

        if admin_partner.id == partner.id:
            domain = []
        else:
            domain = [('partner_id','=',partner.id)]

        question_formulier_count = request.env['question.formulier'].search_count(domain)
        pager = portal_pager(
            url="/my/formulier",
            url_args={'date_begin': date_begin, 'date_end': date_end},
            total=question_formulier_count,
            page=page,
            step=self._items_per_page
        )
        # search the purchase orders to display, according to the pager data
        records = QuestionFormulier.search(
            domain,
            limit=self._items_per_page,
            offset=pager['offset']
        )
        request.session['my_formulier_history'] = records.ids[:100]

        values.update({
            'date': date_begin,
            'formuliers': records,
            'page_name': 'Project Formulier',
            'pager': pager,
            'default_url': '/my/formulier',
        })
        return request.render("quotation_images_feedback.portal_my_project_formulier", values)
