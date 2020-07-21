# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

import pytz    # $ pip install pytz
import datetime
from odoo.exceptions import ValidationError
from odoo import models, fields, api, tools

DTFORMAT = tools.DEFAULT_SERVER_DATETIME_FORMAT


class ProjectTask(models.Model):
    _inherit = 'project.task'

    @api.depends('schedule_ids.date_start', 'schedule_ids.date_end')
    def _computeScheduleHours(self):
        for task in self:
            hours = 0
            for schedule in task.schedule_ids:
                if schedule.resource_id.resource_type != 'user': continue
                hours += ((schedule.date_end - schedule.date_start).seconds / 60) / 60.0
            task.hour_count = hours

    @api.depends('planned_hours', 'hour_count')
    def _plan_hours_get(self):
        for task in self:
            if (task.planned_hours > 0.0):
                task.to_plan_hours = round(
                    100.0 * (task.hour_count) / task.planned_hours, 2)
            else: task.to_plan_hours = 0.0

    schedule_ids = fields.One2many(
        'task.schedule', 'task_id', string='Schedule')
    auto_schedule = fields.Boolean(string="Auto schedule", default=True)
    hour_count = fields.Float(string='Schedule Hours',
                              compute='_computeScheduleHours')
    to_plan_hours = fields.Float(compute='_plan_hours_get', 
                                 string='To Plan hours')
    display_reschedule = fields.Boolean()

    @api.constrains('active')
    def checkSchedules(self):
        for task in self:
            if task.schedule_ids:
                raise ValidationError('Warning! This task is scheduled, so'
                    ' you can not archive/Unarchive this task.')

    @api.model
    def action_meeting_create(self):
        '''Create meeting for schedules'''
        resources, mobile, phone, address, custName = '', '', '', '', ''
        deliveryAddress, note = '', ''
        schedules = self.env['task.schedule'].search([('task_id', '!=', False),
            ('meeting_id', '=', False)])
        for schedule in schedules:
            empNames = '\n'.join(
                [x.name for x in schedule.task_id.resource_ids])
            customer = schedule.task_id.partner_id
            notes = schedule.task_id.notes_for_email
            delivery = schedule.partner_shipping_id
            if customer:
                if customer.name:
                    custName = '\n'.join(['Customer Name:', customer.name])
                addressVal = '\n'.join(
                    [x for x in [
                        customer.street,
                        customer.street2,
                        customer.city,
                        customer.zip,
                        customer.state_id.name if customer.state_id else '',
                        customer.country_id.name if customer.country_id else ''
                    ] if x])
                if addressVal:
                    address = '\n' .join(['Address:', addressVal])
                if customer.phone:
                    phone = '\n'.join(['Customer Phone:', customer.phone])
                if customer.mobile:
                    mobile = '\n'.join(['Customer Mobile:', customer.mobile])
            if delivery:
                deliveryAddressVal = '\n'.join(
                    [x for x in [
                        delivery.street,
                        delivery.street2,
                        delivery.city,
                        delivery.zip,
                        delivery.state_id.name if delivery.state_id else '',
                        delivery.country_id.name if delivery.country_id else ''
                    ] if x])
                if deliveryAddressVal:
                    deliveryAddress = '\n' .join(
                        ['Delivery Address:', deliveryAddressVal])
            if empNames: resources = '\n' .join(['Resources:', empNames])
            if notes: note = '\n' .join(['Note:', notes])
            descriptionList = [custName, address, phone, mobile, resources,
                               deliveryAddress, note]
            description = '\n\n'.join([x for x in descriptionList if x])
            if (schedule.resource_id.user_id or
                schedule.resource_id.resource_type != 'material'):
                event = self.env['calendar.event'].create({
                    'name': 'Task - %s' % schedule.task_id.name,
                    'start': schedule.date_start,
                    'stop': schedule.date_end,
                    'state': 'draft',
                    'allday': False,
                    'partner_ids': [[6, False, [
                        schedule.resource_id.user_id.partner_id.id or None]]],
                    'resource_id': schedule.resource_id.id,
                    'description': description,
                    'partner_shipping_id': schedule.partner_shipping_id.id or None,
                    'user_id': schedule.resource_id.user_id.id
                })
                schedule.write({'meeting_id': event.id})

    @api.model
    def leavesInPeriod(self, resource, start, end):
        cr = self.env.cr
        cr.execute("""
            SELECT id FROM resource_calendar_leaves
            WHERE  resource_id = '%s'
            AND (date_from, date_to) OVERLAPS ('%s', '%s')""" % (
            resource.id, start, end))
        return cr.fetchall()

    @api.model
    def schedulesInPeriod(self, resource, start, end):
        cr = self.env.cr
        cr.execute("""
            SELECT id FROM task_schedule
            WHERE  resource_id = '%s'
            AND (date_start, date_end) OVERLAPS ('%s', '%s') """ % (
            resource.id, start, end))
        return cr.fetchall()

    def create_schedule(self, resource, sstart, send):
        '''Create Schedules'''
        sstart = resource.getTzTimeForThisTime(sstart).replace(tzinfo=None)
        send = resource.getTzTimeForThisTime(send).replace(tzinfo=None)
        self.env['task.schedule'].create({
            'name': self.name + ' (' + resource.name + ')',
            'resource_id': resource.id,
            'date_start': sstart,
            'date_end': send,
            'task_id': self.id,
            'partner_shipping_id': self.partner_shipping_id.id or None
        })

    def check_possibility_and_create_schedule(self, resource):
        '''check possibility and create schedules'''
        tz_info = pytz.timezone(self._context.get('tz') or 'utc')
        start = self.date_start.replace(tzinfo=tz_info)
        end = self.date_end.replace(tzinfo=tz_info)
        workingHrs = resource.calendar_id.get_work_hours_count(
            start, end, resource.id)
        scheduleInterval = resource.calendar_id._work_intervals(
            start, end, resource, domain=None)
        for sstart, send, meta in scheduleInterval:
            if sstart > end: continue
            if (send - sstart).seconds < 7200: continue
            if self.leavesInPeriod(resource, sstart, send): continue
            if self.schedulesInPeriod(resource, sstart, send): continue
            self.create_schedule(resource, sstart, send)

    def action_reschedule(self):
        '''Reschedule task, if resource added on task and after that we change
           task's date then we can reschedule task'''
        self.schedule_ids.unlink()
        for resource in self.resource_ids:
            if not resource.calendar_id: continue
            self.check_possibility_and_create_schedule(resource)
        self.display_reschedule = False

    def manageSchedules(self, vals=None):
        '''Manage schedules on task when resource add or remove on task'''
        if vals is None: vals = {}
        if not vals.get('resource_ids'): return vals
        removedResources = list(set(self.resource_ids.ids) -
                                set(vals['resource_ids'][0][2]))
        addedResources = list(set(vals['resource_ids'][0][2]) -
                              set(self.resource_ids.ids))

        # Remove Schedules for removedResources
        self.schedule_ids.filtered(
            lambda schedule: schedule.resource_id.id in removedResources).unlink()
        if addedResources:
            resources = self.env['resource.resource'].browse(addedResources)
        else: return vals

        if not self.auto_schedule: return vals

        for resource in resources:
            if not resource.calendar_id: continue
            schedules = self.schedule_ids.filtered(
                lambda schedule: schedule.resource_id.id == resource.id)
            if schedules: continue
            self.check_possibility_and_create_schedule(resource)
        return vals

    def write(self, vals):
        for rec in self:
            if rec.resource_ids and rec.auto_schedule:
                if 'date_start' in vals or 'date_end' in vals:
                    rec.display_reschedule = True
            vals = rec.manageSchedules(vals)
        return super(ProjectTask, self).write(vals)

    @api.model
    def resource_reschedule(self):
        '''Reschedule task is deadline date either more than 7 days or not
           and end date is less than 7 days then set end date for today + 1
           week and reschedule task for that date
        '''
        today = datetime.datetime.today().replace(hour=0, minute=0, second=0)
        nextWeek = today + datetime.timedelta(days=7)
        tasks = self.env['project.task'].search(
            ['&', ('date_end', '<', nextWeek.strftime(DTFORMAT)),
             '|', ('date_deadline', '=', None),
                  ('date_deadline', '>', nextWeek)])
        for task in tasks:
            task.date_end = task.date_end + datetime.timedelta(days=7)
            task.action_reschedule()

    # There is no stage with this name in odoo12 so no use of this cron job
    # method in odoo 13

    # @api.model
    # def stage_change(self):
    #     todayDate = datetime.datetime.today()
    #     Facturen = self.stage_id.search([('name', '=', 'Facturen')])
    #     Gepalnd = self.stage_id.search([('name', '=', 'Gepland')])
    #     Planned = self.stage_id.search([('name', '=', 'Planned - xx')])
    #     tasks = self.env['project.task'].search([
    #         ('date_end', '<', todayDate.strftime(DTFORMAT)),
    #         ('stage_id', 'in', (Gepalnd.id, Planned.id))])
    #     if tasks:
    #         for task in tasks:
    #             task.stage_id = Facturen
