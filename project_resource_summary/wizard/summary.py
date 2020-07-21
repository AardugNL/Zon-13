# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

import datetime
import pytz

from odoo import api, fields, models


from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DTFORMAT
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DFORMAT


class SummaryReport(models.Model):
    _name = "summary.report"
    _description = "Summary Report"

    @api.model
    def get_default_dates(self):
        """set defaullt date today and if get click_date from context then set that date"""
        date = fields.Date.today()
        clickDate = self._context.get('click_date', None)
        if clickDate:
            clickDate = datetime.datetime.strptime(clickDate, DTFORMAT).date()
            date = clickDate.strftime(DFORMAT)
        return date

    date_from = fields.Date(string='Date From', default=get_default_dates)
    date_to = fields.Date(string='Date To', default=get_default_dates)
    task_ids = fields.Many2many('project.task', string='Task')
    schedule_ids = fields.Many2many('task.schedule', string='Schedule')
    leave_ids = fields.Many2many('resource.calendar.leaves', string='Leaves')

    @api.onchange('date_from', 'date_to')
    def fillTask(self):
        """fill tasks, schedules and leaves tabs on change start and end date"""
        timezone = pytz.timezone(self._context.get('tz', False) or self.env.user.tz or 'UTC')
        d_frm = self.date_from
        d_frm = datetime.datetime(d_frm.year, d_frm.month, d_frm.day)
        d_frm = timezone.localize(d_frm).astimezone(pytz.utc).strftime(DTFORMAT)

        d_to = self.date_to
        d_to = datetime.datetime(d_to.year, d_to.month, d_to.day, 23, 59, 59)
        d_to = timezone.localize(d_to).astimezone(pytz.utc).strftime(DTFORMAT)

        cr = self.env.cr
        cr.execute("SELECT id FROM project_task "
                   "WHERE (date_start, date_end) OVERLAPS ('%s', '%s')" % (
                       d_frm, d_to))
        taskIds = [x[0] for x in cr.fetchall()]
        self.task_ids = self.env['project.task'].search(
            [('id', 'in', taskIds)]).ids
        cr.execute("SELECT id FROM task_schedule "
                   "WHERE (date_start, date_end) OVERLAPS ('%s', '%s')" % (
                       d_frm, d_to))
        scheduleIds = [x[0] for x in cr.fetchall()]
        self.schedule_ids = self.env['task.schedule'].search(
            [('id', 'in', scheduleIds)]).ids
        cr.execute("SELECT id FROM resource_calendar_leaves "
                   "WHERE (date_from, date_to) OVERLAPS ('%s', '%s')" % (
                       d_frm, d_to))
        leaveIds = [x[0] for x in cr.fetchall()]
        self.leave_ids = self.env['resource.calendar.leaves'].search(
            [('id', 'in', leaveIds)]).ids
