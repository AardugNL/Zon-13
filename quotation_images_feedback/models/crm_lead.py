# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
import re

class CrmLead(models.Model):
    """ Question Formulier Tab """

    _inherit = "crm.lead"

    question_frm_id = fields.Many2one('question.formulier', string='Project Formulier', readonly=True)
    customer_type = fields.Selection([], string='Question Type')

    soort = fields.Selection(
        string='Soort',
        selection=[('aanbouw', 'aanbouw'), ('hoek', 'hoek'), ('gevel', 'kopgevel'), ('groot deel', 'groot deel')],
        default='aanbouw'
    )

    @api.model
    def create(self, vals):
        res = super(CrmLead,self).create(vals)
        if res.lead_category:
            if res.lead_category.name in ['aanbouw','hoek','gevel','groot deel']:
                res.soort = res.lead_category.name
        return res

    def _convert_opportunity_data(self, customer, team_id=False):
        res = super(CrmLead,self)._convert_opportunity_data(customer, team_id)
        QuestionFormulier = self.env['question.formulier']

        #soort fill-up base on lead category and planned revenue default value set base on soort
        if self.lead_category:
            if self.lead_category.name in ['aanbouw','hoek','gevel','groot deel']:
                self.soort = self.lead_category.name

        partner = self.partner_id or customer
        name = res.get('name') or self.name or ''
        question_frm_id = QuestionFormulier.create({
                                                    'name': name +' PF',
                                                    'partner_id': partner.id or False,
                                                    'street': partner.street or '',
                                                    'street2': partner.street2 or '',
                                                    'zip': partner.zip or '',
                                                    'city': partner.city or '',
                                                    'state_id': partner.state_id.id or False,
                                                    'country_id': partner.country_id.id or False,
                                                    'phone': partner.phone,
                                                    'mobile': partner.mobile,
                                                    'lead_id': self.id,
                                                    'state': 'opportunity',
                                                    })
        self.question_frm_id = question_frm_id
        return res

    def create_project_formulier(self):
        QuestionFormulier = self.env['question.formulier']
        partner = self.partner_id
        name = self.name or ''
        question_frm_id = QuestionFormulier.create({
                                                    'name': name +' PF',
                                                    'partner_id': partner.id or False,
                                                    'street': partner.street or '',
                                                    'street2': partner.street2 or '',
                                                    'zip': partner.zip or '',
                                                    'city': partner.city or '',
                                                    'state_id': partner.state_id.id or False,
                                                    'country_id': partner.country_id.id or False,
                                                    'phone': partner.phone,
                                                    'mobile': partner.mobile,
                                                    'lead_id': self.id,
                                                    'state': 'opportunity',
                                                    })
        self.question_frm_id = question_frm_id
        return True

    def project_formulier_view(self):
        return {
            'name': 'Project Formulier',
            'res_model': 'question.formulier',
            'type': 'ir.actions.act_window',
            'res_id': self.question_frm_id.id,
            'context': {},
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': self.env.ref('quotation_images_feedback.view_question_formulier_form').id,
            'target': '_blank',
            }

    def project_formulier_online(self):
        return {
            'type': 'ir.actions.act_url',
            'url': '/question/formulier/'+str(self.question_frm_id.id),
            'target': '_blank',
            }

