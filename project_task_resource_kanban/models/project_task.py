# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

from odoo import models, api


class ProjectTask(models.Model):
    _inherit = 'project.task'

    @api.model
    def create(self, vals):
        '''Create Task Resource when task create'''
        res = super(ProjectTask, self).create(vals)
        self.env['task.resource'].create({'obj_type': 'task', 'task_id': res.id})
        return res

    def unlink(self):
        '''Delete task resource when delete task'''
        for rec in self:
            taskRes = self.env['task.resource'].search([('task_id', '=', rec.id)])
            taskRes.unlink()
        return super(ProjectTask, self).unlink()
