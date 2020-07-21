# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

import pytz    # $ pip install pytz
import calendar
import datetime
from datetime import timedelta
from odoo.exceptions import except_orm
from odoo import models, fields, api, _, tools
from dateutil.relativedelta import relativedelta

DTFORMAT = tools.DEFAULT_SERVER_DATETIME_FORMAT
DFORMAT = tools.DEFAULT_SERVER_DATE_FORMAT


class ResourceAvailablility(models.Model):
    _name = 'resource.availability'
    _rec_name = 'resource_period'
    _description = 'Resource Availability'

    resource_period = fields.Selection([('this_week', 'This Week'),
                                        ('next_week', 'Next Week'),
                                        ('this_month', 'This Month'),
                                        ('next_month', 'Next Month'),
                                        ('custom', 'Custom')],
                                       default='this_week',
                                       string="Plan Period")
    date_from = fields.Date('From', default=fields.Date.today())
    date_to = fields.Date(
        'To', default=datetime.date.today() + datetime.timedelta(days=6))
    resource_header = fields.Text('Header')
    resource_info = fields.Text('Resource')
    resource_header_date = fields.Text('Date Header')
    resource_header_day = fields.Text('Day Header')
    category_ids = fields.Many2many('hr.employee.category', string='Tags')
    type_user = fields.Boolean(string='Human', default=True)
    type_material = fields.Boolean(string='Material')

    @api.onchange('resource_period')
    def get_date(self):
        '''start and end date set based on plan period field'''
        # TODO : time issue
        now = datetime.date.today()
        if self.resource_period == 'this_week':
            self.date_to = (now -
                            timedelta(days=now.weekday())) + timedelta(days=6)
            self.date_from = (now - timedelta(days=now.weekday()))
        elif self.resource_period == 'next_week':
            self.date_from = (now +
                              datetime.timedelta(days=(7 - now.weekday())))
            self.date_to = now + datetime.timedelta(
                days=(7 - now.weekday())) + timedelta(days=6)
        elif self.resource_period == 'this_month':
            month_last_day = calendar.monthrange(now.year, now.month)
            self.date_from = now.replace(day=1)
            self.date_to = now.replace(day=month_last_day[1])
        elif self.resource_period == 'next_month':
            next_month_first_date = now + relativedelta(day=1, months=+1)
            next_month_last_day = calendar.monthrange(
                now.year, next_month_first_date.month)
            self.date_from = next_month_first_date
            self.date_to = (
                next_month_first_date +
                datetime.timedelta(days=next_month_last_day[1] - 1))

    @api.onchange('date_from', 'date_to', 'category_ids', 'type_user', 'type_material')
    def get_resource_availability(self):
        '''resource availability view change based on date and type fields'''
        res = {}
        if (not self.date_from) or (not self.date_to):
            return res
        if self.date_from > self.date_to:
            raise except_orm(
                _('User Error!'),
                _('Please Check Time period Date From can\'t be greater than Date To !'))
        dailyStatusObj = self.env['resource.daily.status']

        def filterResourceStartEnd(d_frm_obj, d_to_obj):
            d_to_obj += datetime.timedelta(days=1)
            cr = self.env.cr
            cr.execute("""
                SELECT id FROM resource_start_end
                WHERE (start_date, end_date) OVERLAPS ('%s', '%s')""" % (
                d_frm_obj.date(), d_to_obj.date()))
            return cr.fetchall()

        def getFilterdResources(start, end):
            """Responsible for considering all valid resources."""
            if self.type_user or self.type_material:
                lines = filterResourceStartEnd(start, end)
                resoDomain = [('calendar_id', '!=', False),
                              ('start_end_ids', 'in', lines)]
                if self.type_material and not self.type_user:
                    resoDomain.append(('resource_type', '=', 'material'))
                if self.type_user and not self.type_material:
                    resoDomain.append(('resource_type', '=', 'user'))
                if self.category_ids:
                    resoDomain.append(('category_ids', 'in', self.category_ids.ids))
                return self.env['resource.resource'].search(resoDomain)

        timezone = pytz.timezone(
            self._context.get('tz', False) or self.env.user.tz or 'UTC')
        d_frm = self.date_from
        d_frm_obj = datetime.datetime(d_frm.year, d_frm.month, d_frm.day)
        d_frm_obj = timezone.localize(d_frm_obj).astimezone(pytz.utc)
        d_to = self.date_to
        d_to_obj = datetime.datetime(d_to.year, d_to.month, d_to.day).replace(hour=23, minute=59)
        d_to_obj = timezone.localize(d_to_obj).astimezone(pytz.utc)
        # Looking for better code. Issue is astimezone and timedelta calculation
        # Calculate from date so diff always should be divided by 86400 (24H).
        daySeconds = 86400
        secondsDiff = (d_to_obj - d_frm_obj).total_seconds()
        # Fall Back
        isFallBack = secondsDiff % daySeconds == 3540
        # Spring Forward
        isSpringFwd = secondsDiff % daySeconds == 82740
        if isFallBack:
            d_to_obj -= datetime.timedelta(hours=1)
        if isSpringFwd:
            d_to_obj += datetime.timedelta(hours=1)

        resource_header_list = []  # _('Employee')]
        date_header_list = []
        day_header_list = []
        header_date = d_frm_obj
        while(header_date <= d_to_obj):
            if isFallBack and date_header_list:
                if (date_header_list[-1]['date'] ==
                        _(header_date.astimezone(timezone).strftime("%d-%b-%y"))):
                    header_date += datetime.timedelta(hours=1)
            date_header_list.append({
                'date': _(header_date.astimezone(timezone).strftime("%d-%b-%y")),
                'org_date': _(header_date.astimezone(timezone).strftime("%Y-%m-%d %H:%M:%S"))
            })
            day_header_list.append(
                _(header_date.astimezone(timezone).strftime("%a")))
            resource_header_list.extend([_('M'), _('E')])
            header_date += datetime.timedelta(days=1)

        # (data, Free, Occupied, Leave, Available, Notapplicable)
        all_resource_detail = []
        sorted_all_resource_detail = []

        view_id = self.env.ref('project_task_schedule.task_schedule_form_occupied').id
        resources = getFilterdResources(d_frm_obj, d_to_obj) or []

        if not resources:
            return

        mapStatus = {
            'Free': 'freeCols',
            'Occupied': 'occcupCols',
            'Leave': 'leaveCols',
            'Available': 'availCols',
            'Notapplicable': 'notappCols',
            'Partial Available': 'occcupCols'
        }
        dailyStatus = dailyStatusObj.search(
            [('resource_id', 'in', resources.ids),
             ('compare_date', '>=', d_frm_obj.astimezone(timezone).strftime(DFORMAT)),
             ('compare_date', '<=', d_to_obj.astimezone(timezone).strftime(DFORMAT))],
            order='dateof')

        all_resource_detail = {}
        for status in dailyStatus:
            resId = status.resource_id.id
            fld = status.res_status.fieldname
            all_resource_detail.setdefault(resId, {
                'name': status.resource_id.name,
                'freeCols': 0,
                'occcupCols': 0,
                'leaveCols': 0,
                'availCols': 0,
                'notappCols': 0,
                'value': [],
                'id': resId})
            dataIds = fld and getattr(status, fld) or []
            all_resource_detail[resId]['value'].append({
                'state': status.res_status.name,
                'date': status.dateof.strftime(DTFORMAT),
                'resource_id': resId,
                'employee_id': resId,
                'data_model': status.res_status.modelname,
                'data_id': dataIds and dataIds.ids[0] or '',
                'view_id': (status.res_status.view_id and
                            status.res_status.view_id.id)
            })
            all_resource_detail[resId][mapStatus[status.res_status.name]] += 1

        all_resource_detail = all_resource_detail.values()
        sorted_all_resource_detail = sorted(
            all_resource_detail,
            key=lambda x: x['freeCols'], reverse=True)
        for x in sorted_all_resource_detail:
            del x['freeCols']
            del x['occcupCols']
            del x['leaveCols']
            del x['availCols']
            del x['notappCols']

        main_header = [{'header': resource_header_list}]
        date_header = [{'head': date_header_list}]
        day_header = [{'head': day_header_list}]
        self.resource_header = str(main_header)
        self.resource_info = str(sorted_all_resource_detail)
        self.resource_header_date = str(date_header)
        self.resource_header_day = str(day_header)
        return res
