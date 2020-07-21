# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

import pytz
import datetime
from odoo.http import request
from odoo.exceptions import except_orm
from odoo import models, fields, api, _, tools

DTFORMAT = tools.DEFAULT_SERVER_DATETIME_FORMAT
DFORMAT = tools.DEFAULT_SERVER_DATE_FORMAT


class TaskResource(models.Model):
    _name = 'task.resource'
    _description = "Task Resource"

    obj_type = fields.Selection([('task', 'Task'), ('resource', 'Resource')],
        string="Types")
    task_id = fields.Many2one('project.task', string='Task')
    resource_id = fields.Many2one('resource.resource', string="Resources")
    start = fields.Datetime('From')
    end = fields.Datetime('To')
    project_id = fields.Many2one(
        'project.project', string='Project', related='task_id.project_id')
    resource_img = fields.Binary('Photo', related='resource_id.resource_image')
    category_ids = fields.Many2many('hr.employee.category', string='Tags',
        related='resource_id.category_ids')
    resource_name = fields.Char('Resource Name', related='task_id.resource_name')
    category_name = fields.Char('Category', compute='_computeCategoryName')
    planned_hours = fields.Float('Planned Hours', related='task_id.planned_hours')
    schedule_hours = fields.Float('Schedule Hours', related='task_id.hour_count')
    task_color = fields.Integer('Task Color Index', compute='_computeTaskColor')
    resource_color = fields.Integer('Resource Color Index',
        compute='_computeResourceColor')

    @api.model
    def getTzTimeForThisTime(self, dtime):
        tzone = pytz.timezone(request.context.get('tz', 'utc') or 'utc')
        if dtime.tzinfo:
            return dtime.astimezone(tzone)
        else:
            dtime = dtime.replace(tzinfo=pytz.timezone('utc'))
        return dtime.astimezone(tzone)

    @api.model
    def isResourcePresent(self, resource, start, end):
        if isinstance(start, str) or isinstance(start, str):
            start = start
        if isinstance(end, str) or isinstance(end, str):
            end = end
        if (end - start).total_seconds() > 365 * 24 * 60 * 60:
            raise except_orm(
                _('User Error!'),
                _('User should not use this view for many days.'))
        start = self.getTzTimeForThisTime(start).replace(tzinfo=None)
        end = self.getTzTimeForThisTime(end).replace(tzinfo=None)
        schedule = resource.calendar_id.get_work_hours_count(
            start, end, compute_leaves=True)
        return bool(schedule)

    @api.model
    def leavesInPeriod(self, resource, start, end):
        cr = self.env.cr
        cr.execute("""
            SELECT id FROM resource_calendar_leaves
            WHERE  resource_id = '%s'
              AND (date_from, date_to) OVERLAPS ('%s', '%s')""" % (
            resource.id, start, end))
        data = cr.fetchall()
        return data

    @api.model
    def schedulesInPeriod(self, resource, start, end):
        cr = self.env.cr
        cr.execute("""
            SELECT id FROM task_schedule
            WHERE  resource_id = '%s'
              AND (date_start, date_end) OVERLAPS ('%s', '%s')""" % (
            resource.id, start, end))
        data = cr.fetchall()
        return data

    @api.model
    def isFullOccupied(self, resource, start, end):
        '''check resource is occupied in specific time duration or not'''
        if isinstance(start, str) or isinstance(start, str):
            start = start
        if isinstance(end, str) or isinstance(end, str):
            end = end

        workingHrs = resource.calendar_id.get_work_hours_count(start, end, resource.id)
        tz_info = pytz.timezone(self._context.get('tz') or 'utc')
        start = start.replace(tzinfo=tz_info)
        end = end.replace(tzinfo=tz_info)
        possibleIntervals = resource.calendar_id._work_intervals(start, end, resource, domain=None)

        possibleWorkSloat = 0
        occupiedStatusForSloat = []
        for pstart, pend, meta in possibleIntervals:
            if pstart > end:
                break
            possibleWorkSloat += 1
            if not self.isResourcePresent(resource, start, end):
                occupiedStatusForSloat.append(True)
            elif self.schedulesInPeriod(resource, pstart, pend):
                occupiedStatusForSloat.append(True)
            elif self.leavesInPeriod(resource, pstart, pend):
                occupiedStatusForSloat.append(True)
            else:
                occupiedStatusForSloat.append(False)
                break

        if possibleWorkSloat == len([x for x in occupiedStatusForSloat if x]):
            return True
        else:
            return False

    # @api.model
    # def getAllResources(self, start, end):
    #     """Responsible for considering all valid resources."""
    #     possible_lines = self.env['resource.start_end'].search(
    #         [('start_date', '<=', start), ('end_date', '>=', end)]).ids
    #     resoDomain = [('calendar_id', '!=', False),
    #                   ('start_end_ids', 'in', possible_lines)]
    #     return self.env['resource.resource'].search(resoDomain)

    def getAvailableResourcesForPeriod(self, start, end, resourceDomain):
        possible_lines = self.env['resource.start_end'].search(
            [('start_date', '<=', start), ('end_date', '>=', end)]).ids
        domain = [('calendar_id', '!=', False),
                  ('start_end_ids', 'in', possible_lines)]
        domain.extend(resourceDomain)
        allResources = self.env['resource.resource'].search(domain)

        available, partialAvailable = [], []
        notAvailabale, applicableForPartial = [], []

        for resource in allResources:
            if not self.isResourcePresent(resource, start, end):
                notAvailabale.append(resource.id)
                continue
            if self.leavesInPeriod(resource, start, end):
                applicableForPartial.append(resource)
            elif self.schedulesInPeriod(resource, start, end):
                applicableForPartial.append(resource)
            else:
                available.append(resource.id)

        for resource in applicableForPartial:
            if self.isFullOccupied(resource, start, end):
                notAvailabale.append(resource.id)
            else:
                partialAvailable.append(resource.id)

        allRes = available + partialAvailable
        return allRes

    def getTasksNeedResourceForPeriod(self, start, end, taskDomain):
        cr = self.env.cr
        cr.execute("""
            SELECT id FROM project_task
            WHERE (date_start, date_end) OVERLAPS ('%s', '%s')""" % (start, end))
        data = cr.fetchall()
        domain = [['id', 'in', [x[0] for x in data]]]
        domain.extend(taskDomain)
        tasks = self.env['project.task'].search(domain).ids
        return tasks

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        # key = field on this record, value = real field on resource record.
        # All conditions will be consedered as or on resource search.
        resourceDummyFieldMap = {
            'resource_id': 'name',
            'category_ids': 'category_ids',
        }
        # key = field on this record, value = real field on task record.
        # All conditions will be consedered as or on task search.
        taskDummyFieldMap = {
            'task_id': 'name'
        }

        isTaskCol, isResourceCol = False, False
        start, end = None, None
        domain, resourceDomain, taskDomain = [], [], []

        def makeStartDay(dt):
            if isinstance(dt, datetime.datetime):
                return dt.replace(hour=0, minute=0, second=0, microsecond=0)

        def makeEndDay(dt):
            if isinstance(dt, datetime.datetime):
                return dt.replace(hour=23, minute=59, second=59, microsecond=999999)

        def isPositiveOperator(operatorStr):
            negSubStrs = ['!', 'not']
            isPositive = True
            for negSubstr in negSubStrs:
                if negSubstr in operatorStr:
                    isPositive = False
                    break
            return isPositive

        # Find task/resourece column and start, end time.
        for condition in args:
            if not hasattr(condition, '__iter__'):
                continue
            if not len(condition) > 2:
                continue

            posCondition = isPositiveOperator(condition[1])

            if condition[0] == 'obj_type' and posCondition:
                if condition[2] == 'task':
                    domain.append(['obj_type', '=', 'task'])
                    isTaskCol = True
                elif condition[2] == 'resource':
                    domain.append(['obj_type', '=', 'resource'])
                    isResourceCol = True

            if condition[0] == 'start' and posCondition:
                start = condition[2]
            if condition[0] == 'end' and posCondition:
                end = condition[2]

        # Need second loop after confirming column
        for condition in args:
            if not hasattr(condition, '__iter__'):
                continue
            if not len(condition) > 2:
                continue

            if condition[0] in resourceDummyFieldMap and isResourceCol:
                if len(resourceDomain):
                    resourceDomain.inseart(-1, '|')
                resourceDomain.append(
                    [resourceDummyFieldMap.get(condition[0]), condition[1], condition[2]])

            if condition[0] in taskDummyFieldMap and isTaskCol:
                if len(taskDomain):
                    taskDomain.inseart(-1, '|')
                taskDomain.append(
                    [taskDummyFieldMap.get(condition[0]), condition[1], condition[2]])

        # Detect does frontend already converted input to UTC.
        isCustomDates = False

        if (isinstance(start, str) or isinstance(start, str)) and (len(start) > 10):
            # start = datetime.datetime.strptime(start, DTFORMAT)
            start = start
            isCustomDates = True
        if (isinstance(start, str) or isinstance(start, str)) and (len(start) <= 10):
            # start = makeStartDay(datetime.datetime.strptime(start, DFORMAT))
            start = makeStartDay(start)
        if (isinstance(end, str) or isinstance(end, str)) and (len(end) > 10):
            # end = datetime.datetime.strptime(end, DTFORMAT)
            end = end
            isCustomDates = True
        if (isinstance(end, str) or isinstance(end, str)) and (len(end) <= 10):
            # end = makeEndDay(datetime.datetime.strptime(end, DFORMAT))
            end = makeEndDay(end)

        if (not start) and (not end):
            start = makeStartDay(datetime.datetime.now())
            end = makeEndDay(start)
        elif start and not end:
            end = makeEndDay(start)
        elif end and not start:
            start = makeStartDay(end)

        if not isCustomDates:
            start = self.getTzTimeForThisTime(
                start.replace(hour=0, minute=0, second=0, microsecond=0)
            ).replace(tzinfo=None)
            end = self.getTzTimeForThisTime(end.replace(
                hour=23, minute=59, second=59, microsecond=999999)
            ).replace(tzinfo=None)

        due_days = (end - start).days
        if due_days > 15:
            raise except_orm(
                _('User Error!'),
                _('Select date between 15 days.'))

        if isResourceCol:
            resources = self.getAvailableResourcesForPeriod(start, end, resourceDomain)
            domain.append(['resource_id', 'in', resources])

        if isTaskCol:
            tasks = self.getTasksNeedResourceForPeriod(start, end, taskDomain)
            domain.append(['task_id', 'in', tasks])

        return super(TaskResource, self).search(domain)

    @api.model
    def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
        # Consider all data.
        dummyDomain = [[u'obj_type', u'!=', u'Undefined']]

        # This is an hack to build kanban column output for all data, we apply
        # real calculation from search. This required for showing empty column
        # and must make call for search so we can return custom data based on
        # customer's special requirement.
        leftDomain = []
        for condition in domain:
            if not hasattr(condition, '__iter__'):
                leftDomain.append(condition)
            if len(condition) > 2 and (dummyDomain[0][0] == condition[0] and
                                       dummyDomain[0][1] == condition[1] and
                                       dummyDomain[0][2] == condition[2]):
                continue
            leftDomain.append(condition)
        res = super(TaskResource, self).read_group(
            dummyDomain, fields, groupby, offset=offset,
            limit=limit, orderby=orderby, lazy=lazy)
        # Inject real domain in response so in search we have information for
        # real search.
        for i, column in enumerate(res):
            res[i]['__domain'] += leftDomain

        return res

    @api.depends('category_ids')
    def _computeCategoryName(self):
        for rec in self:
            name = []
            for category in rec.category_ids:
                name.append(category.name)
            if name:
                rec.category_name = ', '.join(name)
            else:
                rec.category_name = ''

    def _computeTaskColor(self):
        for rec in self:
            if rec.task_id.planned_hours == 0:
                rec.task_color = 0
            elif rec.task_id.planned_hours == rec.task_id.hour_count:
                rec.task_color = 5
            elif rec.task_id.planned_hours != rec.task_id.hour_count:
                rec.task_color = 7

    def _computeResourceColor(self):
        for rec in self:
            rec.resource_color = 0
            # a = self.env['project.task'].search([('id', '=', rec.task_id.id)])
            # if rec.resource_id:
            #     for res in rec.resource_id.start_end_ids:
            #         if a.schedulesInPeriod(rec.resource_id, res.start_date, res.end_date):
            #             rec.resource_color = 7
            #         elif a.leavesInPeriod(rec.resource_id, res.start_date, res.end_date):
            #             rec.resource_color = 7
            #         else:
            #             rec.resource_color = 0

    # def write(self, vals):
    #     if 'dragged-task' in vals:
    #         taskToMerge = vals['dragged-task']
    #         resourceToMerge = vals['resource-id']
    #         self.scheduleResourceOnTask(resource_id=resourceToMerge, task_id=taskToMerge)
    #         del vals['dragged-task']
    #     if 'dragged-resource' in vals:
    #         resourceToMerge = vals['dragged-resource']
    #         taskToMerge = vals['task-id']
    #         self.scheduleResourceOnTask(resource_id=resourceToMerge, task_id=taskToMerge)
    #         del vals['dragged-resource']
    #     return super(TaskResource, self).write(vals)

    def update_task_resource(self, vals):
        if 'dragged-task' in vals:
            taskToMerge = vals['dragged-task']
            resourceToMerge = vals['resource-id']
            self.scheduleResourceOnTask(resource_id=resourceToMerge, task_id=taskToMerge)
            del vals['dragged-task']
        if 'dragged-resource' in vals:
            resourceToMerge = vals['dragged-resource']
            taskToMerge = vals['task-id']
            self.scheduleResourceOnTask(resource_id=resourceToMerge, task_id=taskToMerge)
            del vals['dragged-resource']

    @api.model
    def scheduleResourceOnTask(self, resource_id, task_id):
        resource = self.browse(resource_id)
        task = self.browse(task_id)
        res_id = resource.resource_id
        task_id = task.task_id
        # task_start_date = datetime.datetime.strptime(task_id.date_start, DTFORMAT)
        # task_end_date = datetime.datetime.strptime(task_id.date_end, DTFORMAT)
        task_start_date = task_id.date_start
        task_end_date = task_id.date_end
        for resdate in res_id.start_end_ids:
            if resdate.start_date and resdate.end_date:
                # resource_start_date = datetime.datetime.strptime(resdate.start_date, DFORMAT)
                # resource_end_date = datetime.datetime.strptime(resdate.end_date, DFORMAT)
                resource_start_date = resdate.start_date
                resource_end_date = resdate.end_date
                if task_start_date.date() >= resource_start_date and \
                    task_end_date.date() <= resource_end_date and \
                        res_id.calendar_id:
                    task_id.resource_ids += res_id
                    self.schedulesInPeriod(res_id, resdate.start_date, resdate.end_date)

    @api.model
    def pastTaskResources(self):
        '''Create task resource for thats & resources, which tasks & resource 
           do not have task resource.'''
        resources = self.env['resource.resource'].search([])
        tasks = self.env['project.task'].search([])
        task_resources = self.env['task.resource'].search([])

        doneTaskIds = [x.task_id.id for x in task_resources
                       if x.obj_type == 'task']
        doneResourceIds = [x.resource_id.id for x in task_resources
                           if x.obj_type == 'resource']
        for res in resources:
            if res.id not in doneResourceIds:
                task_resources.create({
                    'obj_type': 'resource',
                    'resource_id': res.id
                })
        for task in tasks:
            if task.id not in doneTaskIds:
                task_resources.create({
                    'obj_type': 'task',
                    'task_id': task.id
                })
