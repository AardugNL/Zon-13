# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

import datetime
import pytz    # $ pip install pytz
import calendar
from dateutil.relativedelta import relativedelta

from odoo import models, fields, api, tools

from odoo.addons.project_resource_status.models import resource_day as Day

DTFORMAT = tools.DEFAULT_SERVER_DATETIME_FORMAT
DFORMAT = tools.DEFAULT_SERVER_DATE_FORMAT


class ResourceStatus(models.Model):
    _name = 'resource.status'
    _description = 'Resource Status'

    def defaultView(self):
        """set default view on view_id field"""
        viewRef = 'project_task_schedule.task_schedule_form_occupied'
        return self.env.ref(viewRef).id

    name = fields.Char(string='Name')
    techname = fields.Char(string='Technical Name')
    modelname = fields.Char(string='Applicable Model')
    view_id = fields.Many2one(
        'ir.ui.view', default=defaultView, string='View')
    fieldname = fields.Char(string='Field of Model on Daily Status')
    # Status color etc.


class ResourceDailyStatus(models.Model):
    _name = 'resource.daily.status'
    _description = 'Resource Daily Status'

    # Main attributes
    resource_id = fields.Many2one('resource.resource', string='Resources', index=True)
    schedule_ids = fields.Many2many('task.schedule', string='Schedule')
    leave_ids = fields.Many2many('resource.calendar.leaves', string='Leave')

    # Period fields
    dateutc = fields.Datetime(string='Date (UTC)')
    dateof = fields.Datetime(string='Date', index=True)
    meridiem = fields.Selection([('am', 'Morning'), ('pm', 'Evening')], string='Meridiem')
    dayof = fields.Char('Schedule Day')
    compare_date = fields.Date(string='Compare Date')

    # Status Information.
    working_hours = fields.Float('Working Hours')
    planned_hours = fields.Float('Planned Hours')
    res_status = fields.Many2one('resource.status', string='Status')

    def resourceStartEndAll(self, d_frm_obj, d_to_obj):
        """get start end date for all resources"""
        d_to_obj += datetime.timedelta(days=1)
        cr = self.env.cr
        cr.execute("""
            SELECT id FROM resource_start_end
            WHERE (start_date, end_date) OVERLAPS ('%s', '%s')""" % (
            d_frm_obj, d_to_obj))
        return cr.fetchall()

    def resourceStartEnd(self, d_frm_obj, d_to_obj, resid):
        """get start end date for specific resource"""
        d_to_obj += datetime.timedelta(days=1)
        cr = self.env.cr
        if not resid:
            return []
        resid = resid if isinstance(resid, int) else resid.id
        cr.execute("""
            SELECT id FROM resource_start_end
            WHERE (start_date, end_date) OVERLAPS ('%s', '%s') and
            resource_id=%s""" % (
            d_frm_obj, d_to_obj, resid))
        return cr.fetchall()

    def leavesInPeriod(self, resourceId, start, end):
        """get resource if he/she on leave"""
        cr = self.env.cr
        cr.execute("""SELECT id FROM resource_calendar_leaves
                      WHERE resource_id = '%s'
                      AND (date_from, date_to) OVERLAPS ('%s', '%s')""" % (
                   resourceId, start, end))
        return [x[0] for x in cr.fetchall()]

    def schedulesInPeriod(self, resourceId, start, end):
        """get resource shedule if he/she is allocated on some task"""
        cr = self.env.cr
        cr.execute(
            """SELECT id FROM task_schedule
               WHERE  resource_id = '%s'
               AND (date_start, date_end) OVERLAPS ('%s', '%s')""" % (
                resourceId, start, end))
        return [x[0] for x in cr.fetchall()]

    @api.model
    def createUpdateResourceStatus(self, records):
        """Make smart move for create or update given record."""
        for vals in records:
            resource_id = vals.get('resource_id', None)
            dayof = vals.get('dayof', None)
            meridiem = vals.get('meridiem', None)
            dateof = vals.get('dateof', None)
            compare_date = vals.get('compare_date', None)

            if not all([resource_id, dayof, meridiem, dateof, compare_date]):
                return

            status = self.search([('resource_id', 'in', [resource_id]),
                                  ('dayof', '=', dayof),
                                  ('compare_date', '=', compare_date),
                                  ('meridiem', '=', meridiem)],
                                 limit=1)
            if not status:
                self.create(vals)
            else:
                status.write(vals)

    @api.model
    def getTimezone(self):
        """get current user timezone"""
        return pytz.timezone(self._context.get('tz', False) or
                             self.env.user.tz or 'UTC')

    @api.model
    def getDateRangeForAllTaskPeriod(self):
        """Responsible to return two dates as following.
        1. smallest of (date_start from project.task records, past 6 months)
        2. highest of (date_end from project.task records. future 6 months)
        """
        timezone = self.getTimezone()

        startTask = self.env['project.task'].search(
            [('date_start', '!=', False)], order='date_start', limit=1)
        d_frm_obj = startTask.date_start
        pastSixMonth = Day.startOfDay(
            datetime.datetime.now() + relativedelta(months=-6))
        d_frm_obj = min(
            pastSixMonth,
            Day.startOfDay(d_frm_obj))
        d_frm_obj = timezone.localize(d_frm_obj).astimezone(pytz.utc)

        endTask = self.env['project.task'].search(
            [('date_end', '!=', False)], order='date_end desc', limit=1)
        d_to_obj = endTask.date_end
        futureSixMonth = Day.endOfDay(
            datetime.datetime.now() + relativedelta(months=6))
        d_to_obj = max(
            futureSixMonth,
            Day.endOfDay(d_to_obj))
        d_to_obj = timezone.localize(d_to_obj).astimezone(pytz.utc)

        return d_frm_obj, d_to_obj

    @api.model
    def durationChunksForPeriod(self, start, end):
        """make duration chunk for start to end date"""
        end = datetime.datetime(end.year, end.month, end.day)
        temp_date = datetime.datetime(start.year, start.month, start.day)
        chunk = [temp_date]
        while (temp_date <= end):
            temp_date += datetime.timedelta(hours=12)
            chunk.append(temp_date)
        return chunk

    @api.model
    def syncResourceForPeriod(self, start, end, resource=None, timezone=None):
        """sync resource for period from start date to end date"""
        if timezone is None:
            timezone = self.getTimezone()
        chunk = self.durationChunksForPeriod(start, end)
        lines = self.resourceStartEndAll(start, end)
        if resource:
            resources = resource
        else:
            resources = self.env['resource.resource'].search(
                [('calendar_id', '!=', False), ('start_end_ids', 'in', lines)])

        calculatedVals = []
        res_status_obj = self.env['resource.status']
        free_id = res_status_obj.search([('techname', '=', 'free')]).id
        available_id = res_status_obj.search(
            [('techname', '=', 'available')]).id
        leave_id = res_status_obj.search([('techname', '=', 'leave')]).id
        occupied_id = res_status_obj.search([('techname', '=', 'occupied')]).id
        notapplicable_id = res_status_obj.search(
            [('techname', '=', 'notapplicable')]).id
        for resc in resources:
            for dStart in chunk[::-1]:
                dEnd = dStart + datetime.timedelta(hours=12)
                leaves = self.leavesInPeriod(resc.id, dStart, dEnd)
                schedules = self.schedulesInPeriod(resc.id, dStart, dEnd)
                workHours = resc.calendar_id.get_work_hours_count(dStart, dEnd, resc.id)
                planHours = 0
                if schedules:
                    planHours = sum([
                        x.planhours or 0 for x in
                        self.env['task.schedule'].browse(schedules)
                    ])
                workingLines = self.resourceStartEnd(dStart, dEnd, resc.id)
                if not workingLines:
                    status = notapplicable_id
                else:
                    status = available_id
                    if leaves and workHours:
                        status = leave_id
                    elif not workHours:
                        status = notapplicable_id
                    elif schedules:
                        status = occupied_id
                    else:
                        status = free_id

                clickDateTime = pytz.utc.localize(dStart).astimezone(timezone)
                clickDateTimeStr = clickDateTime.strftime(DTFORMAT)
                meridiem = dStart.strftime('%p')
                dayof = clickDateTime.strftime("%A")
                vals = {
                    'resource_id': resc.id,
                    'schedule_ids': [(6, 0, schedules)],
                    'leave_ids': [(6, 0, leaves)],
                    'working_hours': workHours,
                    'planned_hours': planHours,
                    'dateof': clickDateTimeStr,
                    'compare_date': clickDateTime.strftime(DFORMAT),
                    'meridiem': meridiem.lower(),
                    'dayof': dayof,
                    'res_status': status
                }
                calculatedVals.append(vals)
        self.createUpdateResourceStatus(calculatedVals)

    @api.model
    def deleteDuplicateResourceStatus(self):
        """Delete resource status those are created duplicate"""
        cr = self.env.cr
        cr.execute("""SELECT string_agg(cast(id AS varchar), ','),
            count(id), resource_id, compare_date, meridiem
            FROM resource_daily_status
            GROUP BY resource_id, compare_date, meridiem""")
        data = cr.fetchall()
        idsToDel = []
        for x in filter(lambda a: a[1] > 1, data):
            idsToDel.extend(eval('[%s]' % x[0])[1:])
        if idsToDel:
            cr.execute('DELETE FROM resource_daily_status WHERE id IN %s' % str(tuple(idsToDel)))

    @api.model
    def getDateRangeForMonthlyTaskPeriod(self):
        """Method is responsible correct date for following criteria.

        i.e. Suppose current month is May than,
        On Monday (0), calculation should be done for Feb
        On Tuesday (1), calculation should be done for March
        On Wednesday (2), calculation should be done for April
        On Thursday (3), calculation should be done for May
        On Friday (4), calculation should be done for June
        On Saturday (5), calculation should be done for July
        On Sunday (6), calculation should be done for August
        """
        timezone = self.getTimezone()
        now = datetime.datetime.today()
        if now.weekday() == 0:
            d_frm_obj = now + relativedelta(months=-3)
            d_to_obj = now + relativedelta(months=-3)
        if now.weekday() == 1:
            d_frm_obj = now + relativedelta(months=-2)
            d_to_obj = now + relativedelta(months=-2)
        if now.weekday() == 2:
            d_frm_obj = now + relativedelta(months=-1)
            d_to_obj = now + relativedelta(months=-1)
        if now.weekday() == 3:
            d_frm_obj = now
            d_to_obj = now
        if now.weekday() == 4:
            d_frm_obj = now + relativedelta(months=+1)
            d_to_obj = now + relativedelta(months=+1)
        if now.weekday() == 5:
            d_frm_obj = now + relativedelta(months=+2)
            d_to_obj = now + relativedelta(months=+2)
        if now.weekday() == 6:
            d_frm_obj = now + relativedelta(months=+3)
            d_to_obj = now + relativedelta(months=+3)

        d_frm_obj = d_frm_obj.replace(day=1, hour=00, minute=00, second=00)
        month_last_day = calendar.monthrange(d_frm_obj.year, d_frm_obj.month)
        d_to_obj = d_to_obj.replace(
            day=month_last_day[1], hour=23, minute=59, second=00)
        d_frm_obj = timezone.localize(d_frm_obj).astimezone(pytz.utc)
        d_to_obj = timezone.localize(d_to_obj).astimezone(pytz.utc)

        return d_frm_obj, d_to_obj

    @api.model
    def calculateAllResourceStatus(self):
        """This cron calculates all data by taking smallest date_start and
        highest date_end from project.task records.
        """
        start, end = self.getDateRangeForAllTaskPeriod()
        self.syncResourceForPeriod(start, end)

    @api.model
    def calculateMonthlyResourceStatus(self):
        """This cronjob re-calculate data for 7 months in 7 days.

        i.e. Suppose current month is May than,
        On Monday (0), calculation should be done for Feb
        On Tuesday (1), calculation should be done for March
        On Wednesday (2), calculation should be done for April
        On Thursday (3), calculation should be done for May
        On Friday (4), calculation should be done for June
        On Saturday (5), calculation should be done for July
        On Sunday (6), calculation should be done for August
        """
        start, end = self.getDateRangeForMonthlyTaskPeriod()
        self.syncResourceForPeriod(start, end)

    @api.model
    def getDateRangeForSmartSyncResources(self):
        """Responsible for calculating date chunks based on updates after last
        run by assuming 30 minutes.
        """
        timezone = self.getTimezone()
        last30Min = datetime.datetime.now() - datetime.timedelta(minutes=30)
        last30MinStr = last30Min.strftime(DTFORMAT)

        schedules = self.env['task.schedule'].search(
            [('write_date', '>=', last30MinStr)])
        leaves = self.env['resource.calendar.leaves'].search(
            [('write_date', '>=', last30MinStr)])

        # Take all chunks and merge chunks and remove period more than 15 days.
        allDates = []
        for schedule in schedules:
            if schedule:
                start = Day.startOfDay(schedule.date_start)
                start = timezone.localize(start).astimezone(pytz.utc)
                end = Day.endOfDay(schedule.date_end)
                end = timezone.localize(end).astimezone(pytz.utc)
                allDates.append([start, end])
        for leave in leaves:
            if leave:
                start = Day.startOfDay(leave.date_from)
                start = timezone.localize(start).astimezone(pytz.utc)
                end = Day.endOfDay(leave.date_to)
                end = timezone.localize(end).astimezone(pytz.utc)
                allDates.append([start, end])

        # Sort chunks and remove chunk which having 15+ days consideration.
        allDateChunks = sorted(allDates, key=lambda lst: lst[0])
        dateChunks = []
        for chunk in allDateChunks:
            if (chunk[1] - chunk[0]).total_seconds() < (16 * 24 * 60 * 60):
                dateChunks.append(chunk)

        # Merge continuous period.
        # i.e. as following
        # twoDayChunks
        # [(dt(2018, 8, 14, 0, 0), dt(2018, 8, 14, 23, 59, 59, 999999)),
        #  (dt(2018, 8, 19, 0, 0), dt(2018, 8, 20, 23, 59, 59, 999999)),
        #  (dt(2018, 8, 21, 0, 0), dt(2018, 8, 22, 23, 59, 59, 999999)),
        #  (dt(2018, 8, 22, 0, 0), dt(2018, 8, 22, 23, 59, 59, 999999)),
        #  (dt(2018, 8, 23, 0, 0), dt(2018, 8, 23, 23, 59, 59, 999999)),
        #  (dt(2018, 8, 24, 0, 0), dt(2018, 8, 24, 23, 59, 59, 999999)),
        #  (dt(2018, 8, 25, 0, 0), dt(2018, 8, 25, 23, 59, 59, 999999)),
        #  (dt(2018, 8, 27, 0, 0), dt(2018, 8, 27, 23, 59, 59, 999999))]
        # mergeChunks
        # [(dt(2018, 8, 14, 0, 0), dt(2018, 8, 14, 23, 59, 59, 999999)),
        #  (dt(2018, 8, 19, 0, 0), dt(2018, 8, 25, 23, 59, 59, 999999)),
        #  (dt(2018, 8, 27, 0, 0), dt(2018, 8, 27, 23, 59, 59, 999999))]
        mergeChunks = []
        skipIndex = []
        for i in range(len(dateChunks)):
            if i in skipIndex:
                continue
            start = dateChunks[i][0]
            end = dateChunks[i][1]

            for j in range(i, len(dateChunks)):
                if ((dateChunks[j][0] - end).total_seconds() <=
                        (24 * 60 * 60)):
                    end = dateChunks[j][1]
                    skipIndex.append(j)
                else:
                    break

            mergeChunks.append((start, end))

        return mergeChunks

    @api.model
    def smartSyncResources(self):
        """Responsible for run cron job that updates status after last
        run by assuming 30 minutes."""
        chunk = self.getDateRangeForSmartSyncResources()
        for start, end in chunk[::-1]:
            self.syncResourceForPeriod(start, end)
