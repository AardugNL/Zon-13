# -*- coding: utf-8 -*-
##############################################################################
#
#
##############################################################################

from datetime import timedelta
from datetime import datetime
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.http import request

class CalendarEvent(models.Model):
    _inherit = "calendar.event"

    question_frm_id = fields.Many2one('question.formulier', string='Project Formulier')

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
            'target': 'current',
            }

    def project_formulier_online(self):
        return {
            'type': 'ir.actions.act_url',
            'url': '/question/formulier/'+str(self.question_frm_id.id),
            'target': 'self',
            }

class CrmLead(models.Model):
    _inherit = "crm.lead"

    def create_meeting(self):
        if self.user_id:
            custName = ''
            address = ''
            phone = ''
            mobile = ''
            note = ''
            formulier = ''
            formulier_alias = ''
            customer = self.partner_id
            if not self.meeting_date:
                raise UserError(_('Please add meeting date!!!.'))
            stop = self.meeting_date + timedelta(hours=2)
            self.opportunity_by = self.user_id
            self.opportunity_date = self.meeting_date
            if customer:
                if customer.name:
                    custName = '\n'.join([_('Customer Name:'), customer.name])
                addressVal = '\n'.join(
                    [x for x in [
                        customer.street,
                        customer.street2,
                        customer.city,
                        customer.zip,
                        customer.state_id.name if customer.state_id else '',
                        customer.country_id.name if customer.country_id else '']
                     if x])
                if addressVal:
                    address = '\n'.join([_('Address:'), addressVal])
                if customer.phone:
                    phone = '\n'.join([_('Customer Phone:'), customer.phone])
                if customer.mobile:
                    mobile = '\n'.join([_('Customer Mobile:'), customer.mobile])
            if self.note:
                note = '\n'.join([_('Opportunity Note:'), self.note])

            if self.question_frm_id:
                self.question_frm_id.date_opportunity = self.meeting_date.date()
                formulierId= str(self.question_frm_id.id)
                formulierLink = request.httprequest.url_root + 'question/formulier/' + formulierId
                formulier = '\n'.join([_('Formulier Url:'), formulierLink])
                if self.question_frm_id.formulier_alias and self.question_frm_id.formulier_alias.alias_domain:
                    alias_name = self.question_frm_id.formulier_alias.alias_name +'@'+ self.question_frm_id.formulier_alias.alias_domain
                    formulier_alias = '\n'.join([_('Alias email:'), alias_name])

            description = '\n\n'.join(
                [x for x in [custName, address, phone, mobile, note, formulier, formulier_alias] if x])
            meeting = {'name': self.name,
                       'start': self.meeting_date,
                       'stop': stop,
                       'opportunity_id': self.id,
                       'state': 'open',
                       'description': description,
                       'question_frm_id': self.question_frm_id.id or False}
            if self.user_id and self.user_id.partner_id:
                meeting.update({'partner_ids': [[6, False, [self.user_id.partner_id.id]]],
                                'user_id': self.user_id.id})
            self.env['calendar.event'].create(meeting)

            activityType = self.env['mail.activity.type'].search([
                ('category', '=', 'meeting')], limit=1)

            stage_id = self.env['crm.stage'].search([('name','in',['Inspectie plannen','Inspectie'])], limit=1)
            if stage_id:
                self.stage_id = stage_id.id
            model = self.env['ir.model'].search([('model', '=', 'crm.lead')], limit=1)
            if model and activityType:
                activity = self.env['mail.activity'].create({
                                 'res_name': self.name,
                                 'activity_type_id': activityType.id,
                                 'summary': activityType.name,
                                 'note': self.note,
                                 'user_id': self.env.user.id,
                                 'res_id': self.id,
                                 'res_model_id': model.id,
                                 'date_deadline': stop.date()
                            })
        else:
            raise UserError(_('Please Select Salesperson!!!.'))
