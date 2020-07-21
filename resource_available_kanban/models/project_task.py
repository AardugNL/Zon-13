# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

import datetime
from datetime import timedelta

from odoo import models, fields, api, tools


DTFORMAT = tools.DEFAULT_SERVER_DATETIME_FORMAT


class ProjectTask(models.Model):
    _inherit = 'project.task'
    _order = 'is_active_on_kanban'

    is_active_on_kanban = fields.Boolean('Active on Kanban')
    is_resource_on_leave = fields.Boolean('Resource on leave')
    resource_on_leave = fields.Char(compute='_get_leaved_resources', string='Fields to use COMPUTED leave')
    is_resource_available = fields.Boolean('Resource available')
    available_resources = fields.Char(compute='_get_available_resources', string='Fields to use COMPUTED')
    display_task = fields.Boolean('Display task', default=True)

    # Set Leaved Resources On Task Based on Resources Daily Status
    def _get_leaved_resources(self):
        leave_id = self.env['resource.status'].search(
            [('techname', '=', 'leave')]).id
        for rec in self:
            if not (rec.date_start and rec.date_end):
                rec.resource_on_leave = ''
                continue
            leaveStatus = self.env['resource.daily.status'].search([
                ('dateof', '>=', rec.date_start.strftime(DTFORMAT)),
                ('dateof', '<=', rec.date_end.strftime(DTFORMAT)),
                ('res_status', '=', leave_id)
            ])
            rec.resource_on_leave = ', '.join(list(set(
                [x.resource_id.name for x in leaveStatus])))
            if not rec.resource_on_leave and rec.is_resource_on_leave:
                rec.display_task = False

    # Set Available Resources On Task Based on Resources Daily Status
    def _get_available_resources(self):
        available_id = self.env['resource.status'].search(
            [('techname', '=', 'free')]).id
        allHuman = self.env['resource.resource'].search(
            [('resource_type', '=', 'user')]).ids
        for rec in self:
            if not (rec.date_start and rec.date_end):
                rec.available_resources = ''
                continue
            availStatus = self.env['resource.daily.status'].search([
                ('dateof', '>=', rec.date_start.strftime(DTFORMAT)),
                ('dateof', '<=', rec.date_end.strftime(DTFORMAT)),
                ('res_status', '=', available_id),
                ('resource_id', 'in', allHuman),
            ])
            rec.available_resources = ', '.join(list(set(
                [x.resource_id.name for x in availStatus])))
            if (not rec.available_resources) and rec.is_resource_available:
                rec.display_task = False

    # create Task Available Resources and Resources On Leave.
    @api.model
    def resourceOnAllocatedTask(self):
        for i in range(30):
            date_start_obj = datetime.datetime.combine(
                (datetime.datetime.now() + datetime.timedelta(days=i)).date(),
                datetime.time(1))
            date_end_obj = datetime.datetime.combine(
                (datetime.datetime.now() + datetime.timedelta(days=i)).date(),
                datetime.time(23))

            taskObj = self.env['project.task']
            tasks = taskObj.search([
                ('date_start', '>=', date_start_obj.strftime(DTFORMAT)),
                ('date_end', '<=', date_end_obj.strftime(DTFORMAT)),
                ('active', '=', False),
                ('is_active_on_kanban', '=', True)
            ])
            if not tasks:
                leaveTask = taskObj.create({
                    'name': 'Resource(s) on Leave',
                    'date_start': date_start_obj.strftime(DTFORMAT),
                    'date_end': date_end_obj.strftime(DTFORMAT),
                    'is_resource_on_leave': True,
                    'active': False,
                    'is_active_on_kanban': True,
                    'color': 5})
                leaveTask.color = 5

                availTask = taskObj.create({
                    'name': 'Available Resources',
                    'date_start': date_start_obj.strftime(DTFORMAT),
                    'date_end': date_end_obj.strftime(DTFORMAT),
                    'is_resource_available': True,
                    'active': False,
                    'is_active_on_kanban': True,
                    'color': 7})
                availTask.color = 7

            update_date_start = (datetime.datetime.combine(
                (datetime.datetime.now() - datetime.timedelta(days=i)).date(),
                datetime.time(1))) - datetime.timedelta(days=1)
            update_start = update_date_start.strftime(DTFORMAT)

        self.env.cr.execute("""
            UPDATE project_task SET is_active_on_kanban = false
            WHERE  date_start <= '%s' and active = false and is_active_on_kanban = true""" % (update_start))
