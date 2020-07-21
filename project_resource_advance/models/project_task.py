# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

import datetime
from datetime import timedelta
from odoo import models, api, tools, _

DTFORMAT = tools.DEFAULT_SERVER_DATETIME_FORMAT


class ProjectTask(models.Model):
    _inherit = 'project.task'

    def kanban_selector(self):
        return {'name': _('Select Employee'),
                'view_mode': 'form',
                'res_model': 'resource.wizard',
                'type': 'ir.actions.act_window',
                'target': 'new'}

    def button_remove_resources(self):
        self.write({'resource_ids': [(5, [], [])]})

    def syncTaskSchedules(self):
        for task in self:
            # ToDo: we can reduce this code by using mapped method direct on task's
            # schedules but here schedules are serched globally so first need
            # to confirm that is that required or not.
            schedules = self.env['task.schedule'].search([('task_id', '=', task.id)])
            expected = set([x.resource_id.id for x in schedules])
            if expected == set(task.resource_ids.ids):
                continue
            else:
                task.write({'resource_ids': [[6, 0, list(expected)]]})

    @api.model
    def manageTaskSchedules(self):
        writeDate = (datetime.datetime.now() - datetime.timedelta(minutes=15)).strftime(DTFORMAT)
        tasks = self.env['project.task'].search([('write_date', '>=', writeDate)])
        tasks.syncTaskSchedules()
