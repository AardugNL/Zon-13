import datetime
import logging
from odoo import api, fields, models, _
from dateutil.relativedelta import relativedelta
from odoo.exceptions import AccessError, Warning
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT
from odoo import SUPERUSER_ID

_logger = logging.getLogger(__name__)

_MAP_COLORS = {
  'oranje': 8,
  'red': 9,
  'green': 7,
  'purple': 6,
}

class CrmLead(models.Model):
    """ CRM Lead Case """
    _inherit = "crm.lead"

    remainder_mail = fields.Boolean(string='FollowUp Mail')
    warning_mail = fields.Boolean(string='Reminder Mail')

    def _get_datetime_fields(self):
        ''' This Function used to mapping datetime fields. '''
        dateTimeFieldList = ['create_date', 'date_action_last', 'date_last_stage_update',
                             'date_closed', 'date_open', 'write_date']
        return dateTimeFieldList

    @api.model
    def create(self, vals):
        existing_partner = [x.partner_id.id for x in self.message_follower_ids]
        res = super(CrmLead, self).create(vals)
        if vals.get('partner_id') and vals.get('partner_id') not in existing_partner:
            partner_id = self.env['res.partner'].browse(vals.get('partner_id'))
            res.message_subscribe(partner_id.ids)
        return res

    def write(self, vals):
        existing_partner = [x.partner_id.id for x in self.message_follower_ids]
        if vals.get('partner_id') and vals.get('partner_id') not in existing_partner:
            partner_id = self.env['res.partner'].browse(vals.get('partner_id'))
            self.message_subscribe(partner_id.ids)
        if 'stage_id' in vals:
            vals.update(remainder_mail=False,
                        warning_mail=False,
                        message_partner_ids=[(4, self.partner_id.id)])
        return super(CrmLead,self).write(vals)

    @api.model
    def send_mail(self, custom):
        Mail = self.env['mail.mail']
        MailMessage = self.env['mail.message']
        for rec in self:
            email_to =  rec.email_from
            partner_id = rec.partner_id and rec.partner_id.id or []
            template = self.env['mail.compose.message'].generate_email_for_composer(custom.template_id.id, rec.id)
            vals = {'auto_delete': False, 'email_to': email_to, 'subject': template.get('subject'), 'body_html': template.get('body')}
            mail_id = Mail.create(vals)
            if not rec.partner_id:
                MailMessage.write({
                    'id':mail_id.mail_message_id.id,
                    'model':'crm.lead',
                    'body': mail_id.body_html,
                    'res_id' : rec.id,
                    'message_type' : 'comment',
                    'subtype_id': self.env['ir.model.data'].xmlid_to_res_id('mail.mt_comment'),
                    'record_name': rec.name,
                  })
            mail_id.send()
            rec.message_post(body=mail_id.body_html,
                              subject=mail_id.subject,
                              message_type='comment',
                              subtype='mail.mt_comment')
            mail_id.unlink()
        return True 

    def compare_date(self, date, after_before, real_date):
        duration, unit = date.split('_')
        if(unit == "m"):
            return real_date + datetime.timedelta(minutes=int(duration))
        hours = int(duration) if unit == "h" else int(duration) * 24
        hours = hours * -1 if after_before == 'before' else hours * 1
        return real_date + datetime.timedelta(hours=hours)

    @api.model
    def email_send_stages(self):
        CrmStage = self.env['crm.stage']
        MailMessage = self.env['mail.message']
        User = self.env['res.users']
        mapDateTimeFields = self._get_datetime_fields()
        if not self.ids:
            CrmStageIds = CrmStage.search([('custom_ids','!=', False)])
            rec_ids = self.search([
                ('type','=','opportunity'),('stage_id', 'in', CrmStageIds.ids)])
            for rec in rec_ids:
                try:
                    for custom in rec.stage_id.custom_ids:
                        when, field, send_mail , mail_action , custom_color, stage = custom.action_when, custom.action_perform, custom.send_mail , custom.mail_action, custom.action_color, custom.crm_stage_id
                        value = getattr(rec, field) if hasattr(rec, field) else False
                        if value:
                            if field in mapDateTimeFields:
                                date = datetime.datetime.strptime(value.strftime('%Y-%m-%d %H:%M:%S'), DEFAULT_SERVER_DATETIME_FORMAT)
                                date_to_compare = self.compare_date(custom.action_time, when, date)
                            else:
                                date = datetime.datetime.strptime(value.strftime('%Y-%m-%d %H:%M:%S'), DEFAULT_SERVER_DATE_FORMAT)
                                date_to_compare = self.compare_date(custom.action_time, when, date)
                            current_date = datetime.datetime.now()
                            if (date >= current_date >= date_to_compare and when == "before") or (when == "after" and current_date >= date_to_compare):
                                if send_mail and mail_action=='remainder' and not rec.remainder_mail:
                                    rec.send_mail(custom)
                                    rec.remainder_mail = True
                                if send_mail and mail_action=='warning' and not rec.warning_mail:
                                    rec.send_mail(custom)
                                    rec.warning_mail = True
                except Exception as e:
                    _logger.error("Error in record <%s>, so skipped this record to fix mail issue ", rec.id)
                    continue

    # @api.multi
    def read(self, fields=None, load='_classic_read'):
        records = super(CrmLead, self).read(fields=fields, load=load)
        crm_stage = self.env['crm.stage']
        mapDateTimeFields = self._get_datetime_fields()
        def compare_date(date, after_before, real_date):
            duration, unit = date.split('_')
            if(unit == "m"):
                return real_date + datetime.timedelta(minutes=int(duration))
            hours = int(duration) if unit == "h" else int(duration) * 24
            hours = hours * -1 if after_before == 'before' else hours * 1
            return real_date + datetime.timedelta(hours=hours)
        # if self.env.context.get('default_type') and self.env.context.get('default_type') == "opportunity":
        for rec in records:
            stage_id =  rec.get('stage_id')[0] if isinstance(rec.get('stage_id'), tuple) else rec.get('stage_id')
            crm_browse = crm_stage.browse(stage_id)
            if rec.get('color') in [6,7,8,9]:rec['color'] = 0
            for custom in crm_browse.custom_ids:
                when, field = custom.action_when, custom.action_perform
                value = rec.get(field)
                if value:
                    if field in mapDateTimeFields:
                        date = datetime.datetime.strptime(value.strftime('%Y-%m-%d %H:%M:%S'), DEFAULT_SERVER_DATETIME_FORMAT)
                        date_to_compare = compare_date(custom.action_time, when, date)
                    else:
                        date = datetime.datetime.strptime(value.strftime('%Y-%m-%d %H:%M:%S'), DEFAULT_SERVER_DATE_FORMAT)
                        date_to_compare = compare_date(custom.action_time, when, date)
                    current_date = datetime.datetime.now()
                    if (date >= current_date >= date_to_compare and when == "before") or (when == "after" and current_date >= date_to_compare):
                        rec['color'] = _MAP_COLORS[custom.action_color]
        return records

class CrmStage(models.Model):
    """ CRM Lead Case """
    _inherit = "crm.stage"

    custom_ids = fields.One2many('crm.stage.custom', 'crm_stage_id', string='Kanban Custom')


class CrmStageCustom(models.Model):
    _name = "crm.stage.custom"
    _order = 'priority desc'
    _description = "CRM Stage Line"

    priority = fields.Integer(string='Priority', default=1, required=True)
    send_mail = fields.Boolean('Send mail')
    template_id = fields.Many2one('mail.template', string='Template')
    crm_stage_id = fields.Many2one('crm.stage', string='Stage')
    action_when = fields.Selection([('before','Before'),('after','After')], string='Before/After', 
        required=True, default='before')
    mail_action = fields.Selection([('remainder','FollowUp Mail'),('warning','Reminder Mail')], string='Mail Action')
    action_time = fields.Selection([
                              ('1_m','1 Minute'),
                              ('5_m','5 Minutes'),
                              ('15_m','15 Minutes'),
                              ('30_m','30 Minutes'),
                              ('1_h','1 Hour'),
                              ('2_h','2 Hours'),
                              ('4_h','4 Hours'),
                              ('8_h','8 Hours'),
                              ('1_d','1 Day'),
                              ('2_d','2 Days'),
                              ('3_d','3 Days'),
                              ('4_d','4 Days'),
                              ('5_d','5 Days'),
                              ('7_d','7 Days'),
                              ('10_d','10 Days'),
                              ('20_d','20 Days'),
                              ('30_d','30 Days'),
                              ('180_d','180 Days'),
                              ('365_d','365 Days'),], string='Time', required=True)
    action_color = fields.Selection([('oranje', 'Oranje'),
                                      ('red','Red'),
                                      ('green','Green'),
                                      ('purple','Purple')], string='Colors', required=True)
    action_perform = fields.Selection([('create_date','Creation Date'),
                                       ('date_action_last','Last Action'),
                                       ('date_closed','Closed'),
                                       ('date_deadline','Expected Closing'),
                                       ('date_open','Assigned'),
                                       ('date_last_stage_update','Last Stage Update'),
                                       ('write_date','Update Date')
                                       ], string='Field', required=True)

    def _get_date_field(self):
        ''' This Function used to mapping date fields. '''
        dateFieldList = ['date_deadline']
        return dateFieldList

    @api.constrains('action_time', 'action_perform')
    def _check_action_time(self):
        for rec in self:
            mapDateField = rec._get_date_field()
            if rec.action_perform in mapDateField and rec.action_time in ['1_m','5_m','15_m','30_m','1_h','2_h','4_h','8_h']:
                raise Warning(_('Misconfiguration, check Field and Time.'))
