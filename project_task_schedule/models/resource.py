# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

from odoo import models, fields, api, _, tools
from odoo.exceptions import except_orm

DTFORMAT = tools.DEFAULT_SERVER_DATETIME_FORMAT
DFORMAT = tools.DEFAULT_SERVER_DATE_FORMAT


class Resource(models.Model):
    _inherit = 'resource.resource'

    def get_overlap_schedules_dates(self, resourceId, start, end):
        cr = self.env.cr
        cr.execute("""
            SELECT date_start, date_end FROM task_schedule
            WHERE resource_id = '%s'
            AND (date_start, date_end) OVERLAPS ('%s', '%s') """ % (
            resourceId, start, end))
        return cr.fetchall()

    # def get_overlap_schedules_ids(self, resourceId, start, end):
    #     cr = self.env.cr
    #     cr.execute("""
    #         SELECT id FROM task_schedule
    #         WHERE  resource_id = '%s'
    #         AND (date_start, date_end) OVERLAPS ('%s', '%s') """ % (
    #         resourceId, start, end))
    #     return cr.fetchall()

    def _compute_partial_timing(self):
        '''calculate allocated resource timing'''
        start = self._context.get('date_start', None)
        end = self._context.get('date_end', None)
        if start and end:
            for record in self:
                occupied = self.get_overlap_schedules_dates(
                    record._origin.id, start, end)
                tzOccupied = []
                for start, end in occupied:
                    start = self.getTzTimeForThisTime(start).replace(tzinfo=None)
                    end = self.getTzTimeForThisTime(end).replace(tzinfo=None)
                    tzOccupied.append(
                        [start.strftime(DTFORMAT), end.strftime(DTFORMAT)])
                dataStr = ' • '.join(
                    [' to '.join([x[0][:-3], x[1][11:-3]]) for x in tzOccupied])
                record.allocated_timing = dataStr

    allocated_timing = fields.Text(compute='_compute_partial_timing')
    schedule_ids = fields.One2many(
        'task.schedule', 'resource_id', string='Schedule')


# this "getConflictPlanning" method is call from cron job for double booked
# but now that code is in comment so no use of this method

# class ResourceLeave(models.Model):
#     _inherit = 'resource.calendar.leaves'

#     @api.model
#     def getConflictPlanning(self):
#         resource = self.resource_id
#         start, end = self.date_from, self.date_to
#         conflictLeaves, conflictSchedules = [], []
#         if resource and start and end:
#             conflictSchedules = self.get_overlap_schedules_ids(
#                 resource.id, start, end)
#             conflictSchedules = self.browse(
#                 [x[0] for x in conflictSchedules if x])
#             cr.execute("""
#                 SELECT id FROM resource_calendar_leaves
#                 WHERE  resource_id = '%s'
#                 AND id NOT IN '%s'
#                 AND (date_from, date_to) OVERLAPS ('%s', '%s') """ % (
#                 resource.id, self.id, start, end))
#             conflictLeaves = cr.fetchall()
#         return conflictSchedules, conflictLeaves


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    locked = fields.Boolean('Locked')
    schedule_id = fields.Many2one('task.schedule', string='Schedule')

    def unlink(self):
        for record in self:
            if record.locked:
                raise except_orm(
                    _('User Error!'),
                    _('This record is not deletable.'))
        return super(AccountAnalyticLine, self).unlink()
