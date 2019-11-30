# -*- coding: utf-8 -*-

import logging
from odoo import fields, http, _, SUPERUSER_ID
from odoo.http import request
import json
import base64

_logger = logging.getLogger(__name__)

class OpportunityForm(http.Controller):

    @http.route(['/opportunity'], type='http', auth='user', website=True)
    def opportunity_details(self, **post):
        countries = request.env['res.country'].sudo().search([])
        Formulier = request.env['question.formulier'].sudo()
        Titles = request.env['res.partner.title'].sudo().search([])
        customer_type = Formulier.fields_get('customer_type')['customer_type']['selection']
        user = request.env.user
        if user.customer_type:
            customer_type = []
            for user_formulier in user.customer_type:
                customer_type.append((user_formulier.technical_name,user_formulier.name))
        values = {
            'Titles': Titles,
            'countries': countries,
            'user': user,
            'customer_type': customer_type
        }
        return request.render('online_opportunity_form.opportunity_template', values)

    @http.route(['/opportunity/create'], type='json', auth="user", methods=['POST'], website=True)
    def opportunity_create(self, data, **kw):
        leadObj = request.env['crm.lead']
        partnerObj = request.env['res.partner']
        lead = leadObj.sudo().create({
            'name': 'Created from website',
            'title': data['title'] or False,
            'lead_category': data['lead_category'] or False,
            'customer_type': data['question_type'],
            'firstname': data['first_name'],
            'lastname': data['last_name'],
            'informal_salutation': 'best',
            'formal_salutation': 'dear',
            'street': data['street'],
            'zip': data['zip'],
            'city': data['city'],
            'country_id': data['country'] or False,
            'email_from': data['email'],
            'phone': data['phone'],
            'lead_lead_source': data['lead_lead_source'] or False
        })
        lead._onchange_par_formal_salutation()
        lead._onchange_informal_salutation()
        partner_id = False
        if lead.email_from:
            partner_id = partnerObj.sudo().search([('email', '=', lead.email_from)], limit=1).id
        elif lead.contact_name:
            partner_id = partnerObj.sudo().search([('name', 'ilike', '%' + lead.contact_name+'%')], limit=1).id
        if partner_id:
            lead.partner_id = partner_id
        if not partner_id and (lead.partner_name or lead.contact_name):
            partner_id = lead.handle_partner_assignation()[lead.id]
        stage_id = request.env['crm.stage'].sudo().search([('name', 'in', ['Quotes External','Offerte Extern'])]).id
        lead.convert_opportunity(partner_id)
        lead.sudo().write({'stage_id': stage_id})
        return lead.project_formulier_online()