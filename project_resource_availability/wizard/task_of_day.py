# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

import pytz
import datetime
from odoo import api, fields, models, tools

DTFORMAT = tools.DEFAULT_SERVER_DATETIME_FORMAT
DFORMAT = tools.DEFAULT_SERVER_DATE_FORMAT


class SummaryReport(models.Model):
    _name = "schedule.report"
    _description = "Schedule Report"

    @api.model
    def get_default_dates(self):
        date = fields.Date.today()
        clickDate = self._context.get('click_date', None)
        if clickDate:
            date = clickDate
        return date

    date_from = fields.Date(string='Date From', default=get_default_dates)
    date_to = fields.Date(string='Date To', default=get_default_dates)
    schedule_ids = fields.Many2many('task.schedule', string='Schedule')

    @api.onchange('date_from', 'date_to')
    def fillTask(self):
        timezone = (pytz.timezone(self._context.get('tz', False) or
                    self.env.user.tz or 'UTC'))
        d_frm = self.date_from 
        d_frm = datetime.datetime(d_frm.year, d_frm.month, d_frm.day)
        d_frm = timezone.localize(d_frm).astimezone(pytz.utc).strftime(DTFORMAT)
        d_to = self.date_to
        d_to = datetime.datetime(d_to.year, d_to.month, d_to.day).replace(hour=23, minute=59)
        d_to = timezone.localize(d_to).astimezone(pytz.utc).strftime(DTFORMAT)

        cr = self.env.cr
        cr.execute("SELECT id FROM task_schedule "
                   "WHERE (date_start, date_end) OVERLAPS ('%s', '%s')" % (
                       d_frm, d_to))
        scheduleIds = [x[0] for x in cr.fetchall()]
        self.schedule_ids = self.env['task.schedule'].search(
            [('id', 'in', scheduleIds)]).ids
