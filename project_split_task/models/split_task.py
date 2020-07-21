# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

import pytz    # $ pip install pytz
import datetime
from odoo.http import request
from datetime import timedelta
from odoo import models, fields, api, tools

DTFORMAT = tools.DEFAULT_SERVER_DATETIME_FORMAT
DFORMAT = tools.DEFAULT_SERVER_DATE_FORMAT


class ProjectTask(models.Model):
    _inherit = 'project.task'

    @api.depends('date_start', 'date_end')
    def _computeHideSplit(self):
        '''Update hide split field value'''
        for task_id in self:
            if task_id.date_start and task_id.date_end:
                if (task_id.date_end - task_id.date_start).days < 1:
                    task_id.hide_split = True
                else:
                    task_id.hide_split = False
            else:
                task_id.hide_split = True

    hide_split = fields.Boolean(string='Hide split', compute='_computeHideSplit')

    @api.model
    def getTzTimeForThisTime(self, dtime):
        tzone = pytz.timezone(request.context.get('tz', 'utc') or 'utc')
        if dtime.tzinfo:
            return dtime.astimezone(tzone)
        return dtime.replace(tzinfo=pytz.timezone('utc')).astimezone(tzone)

    def action_split_task(self):
        '''Split task with button ifsplit 2 button is used then task create for
           only week days otherwise task create for all days between start & end
           date'''
        self.schedule_ids.unlink()
        date_from = self.date_start
        date_to = self.date_end
        
        delta = date_to - date_from
        for i in range(delta.days + 1):
            date_start_obj = datetime.datetime.combine(
                (date_from + datetime.timedelta(days=i)).date(),
                datetime.time(8))
            date_end_obj = datetime.datetime.combine(
                (date_from + datetime.timedelta(days=i)).date(),
                datetime.time(17))
            # start_variable = self.getTzTimeForThisTime(date_start_obj)
            start = self.getTzTimeForThisTime(date_start_obj).replace(tzinfo=None)
            end = self.getTzTimeForThisTime(date_end_obj).replace(tzinfo=None)
            if self._context.get('split2') and start.weekday() in [5, 6]:
                continue
            task = self.create({
                'name': self.name + ' - ' + date_start_obj.strftime(DFORMAT),
                'project_id': self.project_id.id,
                'user_id': self.user_id.id,
                'planned_hours': self.planned_hours,
                'date_start': start,
                'date_end': end,
                'date_deadline': self.date_deadline,
                'tag_ids': [(6, 0, self.tag_ids.ids)],
                'date_finished': self.date_finished,
                'description': self.description,
                'resource_ids': [(6, 0, self.resource_ids.ids)],
                'sequence': self.sequence,
                'partner_id': self.partner_id.id,
                'displayed_image_id': self.displayed_image_id.id,
                'date_assign': self.date_assign,
                'date_last_stage_update': self.date_last_stage_update,
                'auto_schedule': self.auto_schedule,
                'notes_for_email': self.notes_for_email,
                'company_id': self.company_id.id,
            })
            task.action_reschedule()
        self.active = False
        return task

    # def action_split_task2(self):
    #     self.schedule_ids.unlink()
    #     date_from = self.date_start
    #     date_to = self.date_end

    #     delta = date_to - date_from
    #     for i in range(delta.days + 1):
    #         date_start_obj = datetime.datetime.combine(
    #             (date_from + datetime.timedelta(days=i)).date(),
    #             datetime.time(8))
    #         date_end_obj = datetime.datetime.combine(
    #             (date_from + datetime.timedelta(days=i)).date(),
    #             datetime.time(17))
    #         start = self.getTzTimeForThisTime(date_start_obj).replace(tzinfo=None)
    #         end = self.getTzTimeForThisTime(date_end_obj).replace(tzinfo=None)
    #         # Only create task for weekdays.
    #         if start.weekday() in [5, 6]:
    #             continue
    #         task = self.create({
    #             'name': self.name + ' - ' + date_start_obj.strftime(DFORMAT),
    #             'project_id': self.project_id.id,
    #             'user_id': self.user_id.id,
    #             'planned_hours': self.planned_hours,
    #             'date_start': start,
    #             'date_end': end,
    #             'date_deadline': self.date_deadline,
    #             'tag_ids': [(6, 0, self.tag_ids.ids)],
    #             'date_finished': self.date_finished,
    #             'description': self.description,
    #             'resource_ids': [(6, 0, self.resource_ids.ids)],
    #             'sequence': self.sequence,
    #             'partner_id': self.partner_id.id,
    #             'displayed_image_id': self.displayed_image_id.id,
    #             'date_assign': self.date_assign,
    #             'date_last_stage_update': self.date_last_stage_update,
    #             'auto_schedule': self.auto_schedule,
    #             'notes_for_email': self.notes_for_email,
    #             'company_id': self.company_id.id,
    #         })
    #         task.action_reschedule()
    #     self.active = False
    #     return task
