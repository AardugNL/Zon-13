# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

import pytz    # $ pip install pytz
import base64
import datetime
from odoo import models, fields, api, modules, tools

DTFORMAT = tools.DEFAULT_SERVER_DATETIME_FORMAT
DFORMAT = tools.DEFAULT_SERVER_DATE_FORMAT


class ResourceSchedule(models.Model):
    _name = 'task.schedule'
    _description = 'Task Schedule'

    @api.model
    def timesheet_create(self):
        '''Timesheet Create for past schedules'''
        todayDate = datetime.datetime.today()
        schedules = self.env['task.schedule'].search([
            ('date_start', '<', todayDate.strftime(DTFORMAT)),
            '|', ('timesheet_id', '=', False),
            '&', ('timesheet_id', '!=', False),
            ('timesheet_id.locked', '=', False)])
        hours = 0
        for schedule in schedules:
            timesheet = schedule.timesheet_id or None
            start = schedule.date_start
            end = schedule.date_end
            hours = ((end - start).seconds / 60) / 60.0
            vals = {'name': schedule.task_id.name,
                    'date': start,
                    'user_id': schedule.resource_id.user_id.id,
                    'task_id': schedule.task_id.id,
                    'unit_amount': hours,
                    'project_id': schedule.task_id.project_id.id,
                    'schedule_id': schedule.id}
            if not timesheet:
                timesheet = self.env['account.analytic.line'].create(vals)
            schedule.write({'timesheet_id': timesheet.id})
            if start < todayDate: schedule.write({'locked': True})
            if (timesheet.schedule_id and
                timesheet.date + datetime.timedelta(days=1) < todayDate.date()):
                timesheet.write({'locked': True})

    def defClientEight(self):
        context_tz = pytz.timezone(self.env.user.tz or 'UTC')
        start = datetime.datetime.combine(datetime.datetime.now().date(),
                                          datetime.time(8))
        return context_tz.localize(start).astimezone(pytz.UTC).strftime(DTFORMAT)

    def defClientTwelve(self):
        context_tz = pytz.timezone(self.env.user.tz or 'UTC')
        start = datetime.datetime.combine(datetime.datetime.now().date(),
                                          datetime.time(17))
        return context_tz.localize(start).astimezone(pytz.UTC).strftime(DTFORMAT)

    name = fields.Char()
    resource_id = fields.Many2one(
        'resource.resource', string='Resource', required=True)
    date_start = fields.Datetime(
        string='Start Date', required=True, default=defClientEight)
    date_end = fields.Datetime(
        string='End Date', required=True, default=defClientTwelve)
    planhours = fields.Float('Plan Hours', compute='_computePlanHours',
                             store=True)
    task_id = fields.Many2one('project.task', 'Task', ondelete='restrict')
    meeting_id = fields.Many2one('calendar.event', string='Meeting')
    current_date = fields.Datetime(default=fields.Datetime.today())
    task_date_start = fields.Datetime(
        string='Task Date Start', related='task_id.date_start')
    task_date_end = fields.Datetime(
        string='Task Date End', related='task_id.date_end')
    raw_color = fields.Selection([('normal', 'Normal'),
        ('outofrange', 'Out of range'), ('conflict', 'Conflict')],
        string='Raw Color', default='normal', compute='_compute_raw_color')
    status_icon = fields.Binary(attachment=True, help='Double Book Entry')
    timesheet_id = fields.Many2one('account.analytic.line', 'Timesheet')
    locked = fields.Boolean('Locked')
    partner_shipping_id = fields.Many2one('res.partner',
                                          string='Delivery Address')
    # ***********************************
    # This Filed put in comment because there is no use  is in resource
    # management flow added in view but that is also invisible so also put cron
    # for this field in comment
    # ***********************************

    # double_booked = fields.Boolean(
    #     'Is Double Booked', compute='_compute_raw_color', store=True)

    def _computePlanHours(self):
        for record in self:
            record.planhours = (record.date_end - record.date_start).total_seconds() / 60 / 60 

    # below mehtods are in comment because there no use of this methods
    # because double_booked field remove from code

    # @api.model
    # def getConflictPlanning(self):
    #     resource = self.resource_id
    #     start, end = self.date_start, self.date_end
    #     conflictSchedules, conflictLeaves = [], []
    #     if resource and start and end:
    #         cr = self.env.cr
    #         cr.execute(
    #             """SELECT id FROM task_schedule
    #                WHERE  resource_id = '%s'
    #                  AND id NOT IN ('%s')
    #                  AND (date_start, date_end) OVERLAPS ('%s', '%s')""" % (
    #                 resource.id, self.id, start, end))
    #         conflictSchedules = cr.fetchall()
    #         conflictSchedules = self.browse(
    #             [x[0] for x in conflictSchedules if x])
    #         cr.execute(
    #             """SELECT id FROM resource_calendar_leaves
    #                WHERE  resource_id = '%s'
    #                  AND (date_from, date_to) OVERLAPS ('%s', '%s')""" % (
    #                 resource.id, start, end))
    #         conflictLeaves = cr.fetchall()
    #     return conflictSchedules, conflictLeaves

    # @api.model
    # def cron_double_booked_quick(self):
    #     guessPreviousRun = (
    #         datetime.datetime.now() + datetime.timedelta(minutes=-6)
    #     ).strftime(DTFORMAT)

    #     schedules = self.search([('write_date', '>=', guessPreviousRun)])
    #     leaves = self.env['resource.calendar.leaves'].search(
    #         [('write_date', '>=', guessPreviousRun)])

    #     for schedule in schedules:
    #         conflictSchedules, conflictLeaves = schedule.getConflictPlanning()
    #         if conflictSchedules or conflictLeaves:
    #             if conflictSchedules:
    #                 for x in conflictSchedules:
    #                     x.double_booked = True
    #             schedule.double_booked = True
    #         else:
    #             schedule.double_booked = False

    #     for leave in leaves:
    #         conflictSchedules, conflictLeaves = leave.getConflictPlanning()
    #         if conflictSchedules:
    #             for x in conflictSchedules:
    #                 x.double_booked = True

    #     return True

    # @api.model
    # def cron_double_booked_daily(self):
    #     prevDayStart = (
    #         datetime.datetime.now() + datetime.timedelta(days=-1)
    #     ).replace(hour=0, minute=0, second=0).strftime(DTFORMAT)
    #     schedules = self.search([('write_date', '>=', prevDayStart)])
    #     leaves = self.env['resource.calendar.leaves'].search(
    #         [('write_date', '>=', prevDayStart)])

    #     # When all schedules need recalculation
    #     # schedules = self.search([])
    #     # leaves = self.env['resource.calendar.leaves'].search([])

    #     for schedule in schedules:
    #         conflictSchedules, conflictLeaves = schedule.getConflictPlanning()
    #         if conflictSchedules or conflictLeaves:
    #             if conflictSchedules:
    #                 for x in conflictSchedules:
    #                     x.double_booked = True
    #             schedule.double_booked = True
    #         else:
    #             schedule.double_booked = False

    #     for leave in leaves:
    #         conflictSchedules, conflictLeaves = leave.getConflictPlanning()
    #         if conflictSchedules:
    #             for x in conflictSchedules:
    #                 x.double_booked = True

    #     return True

    @api.model
    def create(self, vals):
        result = super(ResourceSchedule, self).create(vals)
        if not result.name:
            result.name = '%s (%s)' % (result.task_id.name,
                                       result.resource_id.name)
        return result

    def write(self, vals):
        '''write schedule name and meeing name , partners & resouurce'''
        if vals and self.meeting_id:
            task, resource = vals.get('task_id'), vals.get('resource_id')
            start, end = vals.get('date_start'), vals.get('date_end')
            if task and resource:
                res = self.resource_id.browse(resource)
                if res.user_id or res.resource_type != 'material':
                    taskName = self.task_id.browse(task)
                    self.name = taskName.name + ' (' + res.name + ')'
                    self.meeting_id.write({
                        'partner_ids': [[6, False, [res.user_id.partner_id.id]]],
                        'resource_id': res.id,
                        'name': 'Task - %s' % taskName.name
                    })
            if not task and resource:
                res = self.resource_id.browse(resource)
                if res.user_id or res.resource_type != 'material':
                    self.name = self.task_id.name + ' (' + res.name + ')'
                    self.meeting_id.write({
                        'partner_ids': [[6, False, [res.user_id.partner_id.id]]],
                        'resource_id': res.id
                    })
            if not resource and task:
                taskName = self.task_id.browse(task)
                self.name = taskName.name + ' (' + self.resource_id.name + ')'
                self.meeting_id.write({'name': 'Task - %s' % taskName.name})
            self.meeting_id.write({'start': start or self.date_start,
                                   'stop': end or self.date_end})
        return super(ResourceSchedule, self).write(vals)

    def _compute_raw_color(self):
        ''''Find conflict records'''
        for record in self:
            cr = self.env.cr
            cr.execute("""
                SELECT id FROM task_schedule
                WHERE  resource_id = '%s'
                AND (date_start, date_end) OVERLAPS ('%s', '%s')""" % (
                record.resource_id.id, record.date_start, record.date_end))
            conflict = cr.fetchall()
            length = len(conflict)
            cr.execute("""
                SELECT id FROM resource_calendar_leaves
                WHERE  resource_id = '%s'
                  AND (date_from, date_to) OVERLAPS ('%s', '%s')""" % (
                record.resource_id.id, record.date_start, record.date_end))
            leaves = cr.fetchall()
            length += len(leaves)
            if length > 1:
                image_path = modules.get_module_resource(
                    'project_task_schedule', 'static/src/img', 'conflict.png')
                conflictImg = base64.b64encode(open(image_path, 'rb').read())
                record.status_icon = conflictImg
                record.raw_color = 'conflict'
                # record.double_booked = True
                continue
            elif length == 1:
                record.raw_color = 'normal'
                # record.double_booked = False
                continue

    def unlink(self):
        for record in self:
            if record.meeting_id: record.meeting_id.unlink()
        return super(ResourceSchedule, self).unlink()
