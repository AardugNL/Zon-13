# -*- coding: utf-8 -*-
##############################################################################
#
#
##############################################################################

from datetime import timedelta

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class Crm_Lead(models.Model):
    _inherit = "crm.lead"

    meeting_date = fields.Datetime(string="Meeting date", help="Customer Meeting Start Date", default=fields.Datetime.now)
    note = fields.Text()

    def create_meeting(self):
        if self.user_id:
            custName = ''
            address = ''
            phone = ''
            mobile = ''
            note = ''
            customer = self.partner_id
            stop = self.meeting_date + timedelta(hours=2)
            self.opportunity_by = self.user_id
            if self.meeting_date:
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
                    address = '\n'.join(['Address:', addressVal])
                if customer.phone:
                    phone = '\n'.join(['Customer Phone:', customer.phone])
                if customer.mobile:
                    mobile = '\n'.join(['Customer Mobile:', customer.mobile])
            if self.note:
                note = '\n'.join(['Opportunity Note:', self.note])

            description = '\n\n'.join(
                [x for x in [custName, address, phone, mobile, note] if x])
            meeting = {'name': self.name,
                       'start': self.meeting_date,
                       'stop': stop,
                       'opportunity_id': self.id,
                       'state': 'open',
                       'description': description}

            if self.user_id and self.user_id.partner_id:
                meeting.update({'partner_ids': [[6, False, [self.user_id.partner_id.id]]],
                                'user_id': self.user_id.id})
            self.env['calendar.event'].create(meeting)

            activityType = self.env['mail.activity.type'].search([
                ('category', '=', 'meeting')], limit=1)
            stage_id = self.env.ref('opportunity_meeting.stage_lead_appoinment')
            if not stage_id:
                stage_id = self.env['crm.stage'].search([('name','in',['Appointment','Afspraak'])], limit=1)
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
