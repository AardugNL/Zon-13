# -*- coding: utf-8 -*-
##############################################################################
#
#
##############################################################################

from odoo import models, fields, api
from datetime import datetime


class LogActivity(models.Model):
    _name = 'activity.log'
    _description = 'Describe Activity Log'

    name = fields.Char(related='opportunity_id.name', string='Name')
    opportunity_id = fields.Many2one('crm.lead', string='Opportunity')
    stage = fields.Char(string="Stage Name")
    date = fields.Datetime(string="Last Update Date", default=fields.Datetime.now)
    activity_ids = fields.Many2many('mail.activity.type' , 'log_activity_rel',
                    'oppotunity_activity', 'log_activity_id', string='Activities')
    login_user = fields.Many2one('res.users',  string='Login User')
    privious_stage = fields.Char(string="Privious Stage")
    notes = fields.Char(string="Note")

class LeadActivity(models.Model):
    _inherit = 'crm.lead'

    @api.model
    def create(self, vals):
        record = super(LeadActivity, self).create(vals)
        self.env['activity.log'].create({
                'opportunity_id': record.id,
                'stage': record.stage_id.name,
                'date': datetime.today(),
                'activity_ids': [(6, 0, [activity.activity_type_id.id for activity in self.activity_ids]) ],
                'login_user': self.env.user.id,
                'notes' : 'Opportunity Create',
        })
        return record

    # @api.multi
    def write(self, vals):
        stageId = self.env['crm.stage'].browse(vals.get('stage_id'))
        if stageId:
            self.env['activity.log'].create({
                'opportunity_id': self.id,
                'stage': stageId.name,
                'date': datetime.today(),
                'activity_ids': [(6, 0, [activity.activity_type_id.id for activity in self.activity_ids]) ],
                'login_user': self.env.user.id,
                'privious_stage': self.stage_id.name,
                'notes' : 'Stage changed from ' + self.stage_id.name+ ' to ' +stageId.name
            })
        return super(LeadActivity, self).write(vals)
