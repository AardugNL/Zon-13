# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

import pytz    # $ pip install pytz
import logging
import datetime
from odoo.http import request
from odoo.exceptions import except_orm
from odoo import models, fields, api, _, tools

_logger = logging.getLogger(__name__)
DTFORMAT = tools.DEFAULT_SERVER_DATETIME_FORMAT
DFORMAT = tools.DEFAULT_SERVER_DATE_FORMAT


class ResourceWizard(models.TransientModel):
    _name = 'resource.wizard'
    _description = 'Resource Wizard'

    # Performance Cache
    customCache = {'time': datetime.datetime.now().replace(second=00,
                                                     microsecond=00)}

    def _default_task(self):
        return self.env['project.task'].browse(self._context.get('active_id'))

    @api.model
    def getActiveTask(self):
        if self._context.get('active_id'):
            task = self.env['project.task'].browse(
                self._context.get('active_id'))
        else:
            task = self.task_id
        return task

    @api.depends('task_id')
    def _default_selected_resources(self):
        task = self.getActiveTask()
        if not task:
            _logger.warning('Can not get resources because Task not found.')
        return task.resource_ids

    @api.model
    def getStartEnd(self):
        return (self._context.get('date_start', self.date_start),
                self._context.get('date_end', self.date_end))

    @api.model
    def getTzTimeForThisTime(self, dtime, tz):
        tzone = pytz.timezone(request.context.get('tz', 'utc') or 'utc')
        if dtime.tzinfo:
            return dtime.astimezone(tzone)
        else:
            dtime = dtime.replace(tzinfo=pytz.timezone('utc'))
        return dtime.astimezone(tzone)

    @api.model
    def isResourcePresent(self, resource, start, end):
        if isinstance(start, str) or isinstance(start, unicode):
            start = datetime.datetime.strptime(start, DTFORMAT)
        if isinstance(end, str) or isinstance(end, unicode):
            end = datetime.datetime.strptime(end, DTFORMAT)
        if (end - start).total_seconds() > 365 * 24 * 60 * 60:
            raise except_orm(
                _('User Error!'),
                _('User should not auto schedule task for many days.'))
        start = self.getTzTimeForThisTime(start, 'UTC').replace(tzinfo=None)
        end = self.getTzTimeForThisTime(end, 'UTC').replace(tzinfo=None)
        schedule = resource.calendar_id.get_working_hours(
            start, end, compute_leaves=True, resource_id=resource.id)
        return bool(schedule)

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
            AND (date_start, date_end) OVERLAPS ('%s', '%s')""" % (
            resource.id, start, end))
        return cr.fetchall()

    @api.model
    def isFullOccupied(self, resource, start, end):
        if isinstance(start, str) or isinstance(start, unicode):
            start = datetime.datetime.strptime(start, DTFORMAT)
        if isinstance(end, str) or isinstance(end, unicode):
            end = datetime.datetime.strptime(end, DTFORMAT)

        workingHrs = resource.calendar_id.get_work_hours_count(start, end, resource.id)
        tz_info = pytz.timezone(self._context.get('tz') or 'utc')
        start = start.replace(tzinfo=tz_info)
        end = end.replace(tzinfo=tz_info)
        possibleIntervals = resource.calendar_id._work_intervals(
            start, end, resource, domain=None)
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

    @api.model
    def getAllResources(self, start, end):
        """Responsible for considering all valid resources."""
        possible_lines = self.env['resource.start_end'].search(
            [('start_date', '<=', start), ('end_date', '>=', end)]).ids
        resoDomain = [('calendar_id', '!=', False),
                      ('start_end_ids', 'in', possible_lines)]
        if self.type_material and not self.type_user:
            resoDomain.append(('resource_type', '=', 'material'))
        if self.type_user and not self.type_material:
            resoDomain.append(('resource_type', '=', 'user'))
        if self.category_ids:
            resoDomain.append(('category_ids', 'in', self.category_ids.ids))
        return self.env['resource.resource'].search(resoDomain)

    @api.model
    def getResources(self):
        """Responsible for finding partial available resources."""
        def getStartChunk(start):
            if isinstance(start, str) or isinstance(start, unicode):
                start = datetime.datetime.strptime(start, DTFORMAT)
            newHour, newMinute = (00, 00) if start.hour < 12 else (12, 00)
            start = start.replace(hour=newHour, minute=newMinute, second=0)
            return start.strftime(DTFORMAT)

        def getEndChunk(end):
            if isinstance(end, str) or isinstance(end, unicode):
                end = datetime.datetime.strptime(end, DTFORMAT)
            newHour, newMinute = (11, 59) if end.hour < 12 else (23, 59)
            end = end.replace(hour=newHour, minute=newMinute, second=59)
            return end.strftime(DTFORMAT)

        start, end = self.getStartEnd()
        if (not start) or (not end):
            return None, None, None, None

        if (not self.type_user) and (not self.type_material):
            return None, None, None, None

        allResources = self.getAllResources(start, end)

        resDailyStatus = self.env['resource.daily.status'].search_read([
            ('resource_id', 'in', allResources.ids),
            ('dateof', '>=', getStartChunk(start)),
            ('dateof', '<=', getEndChunk(end)),
        ], fields=['resource_id', 'res_status'])

        groupByResources = {}
        for rds in resDailyStatus:
            groupByResources.setdefault(rds['resource_id'][0], []).append(rds)

        stMap = {x.techname: x.id
                 for x in self.env['resource.status'].search([])}

        available = []
        partialAvailable = []
        notAvailabale = []
        for resourceId in groupByResources:
            allRSt = [x['res_status'][0] for x in groupByResources[resourceId]]
            if (stMap['free'] in allRSt and
                    stMap['occupied'] not in allRSt and
                    stMap['leave'] not in allRSt):
                available.append(resourceId)
            if stMap['free'] not in allRSt:
                notAvailabale.append(resourceId)
            if (stMap['free'] in allRSt and
                    (stMap['occupied'] in allRSt or stMap['leave'] in allRSt)):
                partialAvailable.append(resourceId)

        return allResources, available, partialAvailable, notAvailabale

    @api.depends('selected_resource_ids')
    def _default_avail_resources(self):
        _, allAvail, _, _ = self.getResources()
        if allAvail is None:
            return
        task = self.getActiveTask()
        avail = list(set(allAvail) - set(task.resource_ids.ids))
        return avail

    @api.depends('selected_resource_ids')
    def _default_partial_resources(self):
        _, _, allPart, _ = self.getResources()
        if allPart is None:
            return
        task = self.getActiveTask()
        part = list(set(allPart) - set(task.resource_ids.ids))
        return part

    @api.depends('selected_resource_ids')
    def _default_not_avail_resources(self):
        _, _, _, allNot = self.getResources()
        if allNot is None:
            return
        task = self.getActiveTask()
        notavail = list(set(allNot) - set(task.resource_ids.ids))
        return notavail

    @api.onchange('selected_resource_ids')
    def _change_selected(self):
        self._manageResource(event='selected_resource_ids')

    @api.onchange('avail_resource_ids')
    def _change_avail(self):
        self._manageResource(event='avail_resource_ids')

    @api.onchange('partial_resource_ids')
    def _change_partial(self):
        self._manageResource(event='partial_resource_ids')

    @api.onchange('not_avail_resource_ids')
    def _change_notavail(self):
        self._manageResource(event='not_avail_resource_ids')

    @api.onchange('category_ids', 'type_material', 'type_user')
    def _change_category(self):
        self._manageResource(event='category_ids')

    def _manageResource(self, event=None):
        resoObj = self.env['resource.resource']
        start, end = self.getStartEnd()
        if (not start) or (not end):
            return

        allRes, allAvail, allPart, allNot = self.getResources()
        allres = allRes.ids if allRes else []
        avail = self.avail_resource_ids.ids
        selected = self.selected_resource_ids.ids
        notavail = self.not_avail_resource_ids.ids
        partial = self.partial_resource_ids.ids

        if event in ['avail_resource_ids', 'partial_resource_ids',
                     'not_avail_resource_ids']:  # Select Resource
            finalSelected = selected + list(
                set(allres) - set(avail) - set(partial) - set(notavail)
            )
            self.selected_resource_ids = resoObj.browse(set(finalSelected))
        elif event in ['selected_resource_ids']:  # Deselect Resource
            deselected = list(
                set(allres) - set(avail) - set(partial) -
                set(notavail) - set(selected)
            )
            if allAvail:
                addToAvail = [x for x in deselected if x in allAvail]
                self.avail_resource_ids = resoObj.browse(list(set(
                    self.avail_resource_ids.ids + addToAvail)))
            if allPart:
                addToPart = [x for x in deselected if x in allPart]
                self.partial_resource_ids = resoObj.browse(list(set(
                    self.partial_resource_ids.ids + addToPart)))
                self.partial_resource_ids._compute_partial_timing()
            if allNot:
                addToNot = [x for x in deselected if x in allNot]
                self.not_avail_resource_ids = resoObj.browse(list(set(
                    self.not_avail_resource_ids.ids + addToNot)))
        elif event in ['category_ids']:  # Filter Used
            selectedFilter = (
                set(self.task_id.resource_ids.ids).union(set(selected))
            ).intersection(set(allres))
            self.selected_resource_ids = resoObj.browse(list(set(selected)))
            self.avail_resource_ids = resoObj.browse(list(
                set(allAvail or []).intersection(set(allres)) - set(selected)
            ))
            self.partial_resource_ids = resoObj.browse(list(
                set(allPart or []).intersection(set(allres)) - set(selected)
            ))
            self.not_avail_resource_ids = resoObj.browse(list(
                set(allNot or []).intersection(set(allres)) - set(selected)
            ))

    task_id = fields.Many2one(
        'project.task', string='Task', required=True, default=_default_task)
    date_start = fields.Datetime(
        string='Start Date', related='task_id.date_start')
    date_end = fields.Datetime(
        string='End Date', related='task_id.date_end')
    avail_resource_ids = fields.Many2many('resource.resource',
        'avail_resource_rel', string='Available Resources',
        default=_default_avail_resources)
    partial_resource_ids = fields.Many2many('resource.resource',
        'partial_resource_rel', string='Partial Resources',
        default=_default_partial_resources)
    not_avail_resource_ids = fields.Many2many('resource.resource',
        'not_resource_rel', string='Not Avail Resources',
        default=_default_not_avail_resources)
    selected_resource_ids = fields.Many2many(
        'resource.resource', string='Selected Resources',
        default=_default_selected_resources)
    category_ids = fields.Many2many('hr.employee.category', string='Tags')
    type_user = fields.Boolean(string='Human', default=True)
    type_material = fields.Boolean(string='Material', default=True)

    @api.model
    def create(self, values):
        task = values.get('task_id', None)
        if not task:
            _logger.warning("Task not selected from Manage Resource Wizard.")
            pass
        else:
            task = self.env['project.task'].browse(task)
            selectedResources = values.get('selected_resource_ids', None)
            _logger.debug("Selected Resources - %s"% (selectedResources))
            # this is not needed it's make issue
            # if selectedResources and len(selectedResources) == 3:
            #     selectedResources = selectedResources[-1]
            task.resource_ids = selectedResources
            # # If issue after super create of wizard than try this.
            # if 'selected_resource_ids' in values:
            #     del values['selected_resource_ids']
        return super(ResourceWizard, self).create(values)

    def save_window_close(self):
        # self.task_id.action_meeting_create()
        return {'type': 'ir.actions.act_window_close', 'auto_refresh': '1'}
