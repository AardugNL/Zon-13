# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

import pytz
from odoo import models, api, tools

from odoo.addons.project_resource_status.models import resource_day as Day

DTFORMAT = tools.DEFAULT_SERVER_DATETIME_FORMAT


class Resource(models.Model):
    _inherit = 'resource.resource'

    def processResourceStatusForPeriod(self):
        '''create resource status from button that on resource form view'''
        if self.start_end_ids:
            for res_date in self.start_end_ids:
                start = Day.startOfDay(res_date.start_date)
                end = Day.endOfDay(res_date.end_date)
                self.env['resource.daily.status'].syncResourceForPeriod(start, end)


class HrHolidays(models.Model):
    _inherit = 'hr.leave'

    def action_approve(self):
        '''make leave status when leave is approved from HR'''
        result = super(HrHolidays, self).action_approve()
        resource_leave = self.env['resource.calendar.leaves'].search(
            [('holiday_id', '=', self.id)])
        resDailyStatusObj = self.env['resource.daily.status']
        timezone = resDailyStatusObj.getTimezone()
        if resource_leave.date_from and resource_leave.date_to:
            start = Day.startOfDay(resource_leave.date_from)
            start = timezone.localize(start).astimezone(pytz.utc)
            end = Day.endOfDay(resource_leave.date_to)
            end = timezone.localize(end).astimezone(pytz.utc)
            resDailyStatusObj.syncResourceForPeriod(start, end)
        return result

class ResourceLeave(models.Model):
    _inherit = 'resource.calendar.leaves'

    def unlink(self):
        '''remove leave status when unlink leave from calendar'''
        for rec in self:
            resDailyStatus = self.env['resource.daily.status'].search(
                [('resource_id', '=', rec.resource_id.id)])
            free_id = self.env['resource.status'].search(
                [('techname', '=', 'free')]).id
            for status in resDailyStatus:
                for leave in status.leave_ids:
                    if (leave.id == rec.id
                        and status.res_status.techname == 'leave'):
                        status.res_status = free_id
        return super(ResourceLeave, self).unlink()

class TaskSchedule(models.Model):
    _inherit = 'task.schedule'

    def write(self, vals):
        '''on changes of start date and end date of shedule change status for it'''
        res = super(TaskSchedule, self).write(vals)
        resDailyStatusObj = self.env['resource.daily.status']
        timezone = resDailyStatusObj.getTimezone()
        if self.date_start and self.date_end:
            start = Day.startOfDay(self.date_start)
            start = timezone.localize(start).astimezone(pytz.utc)
            end = Day.endOfDay(self.date_end)
            end = timezone.localize(end).astimezone(pytz.utc)
            resDailyStatusObj.syncResourceForPeriod(start, end, resource=self.resource_id)
        return res

    def unlink(self):
        '''on delete schedule change free status for that resource'''
        for record in self:
            resDailyStatus = self.env['resource.daily.status'].search(
                [('resource_id', '=', record.resource_id.id)])
            free_id = self.env['resource.status'].search(
                [('techname', '=', 'free')]).id
            for status in resDailyStatus:
                for schedule in status.schedule_ids:
                    if schedule.id == record.id:
                        status.res_status = free_id
        return super(TaskSchedule, self).unlink()
