# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

from odoo import models, fields, api, _
from odoo import SUPERUSER_ID
from odoo.exceptions import UserError


class ProjectTaskTypeInh(models.Model):
    _inherit = 'project.task.type'

    move_allow = fields.Boolean(string='Only Billing Manager Can Move')


class ProjectTask(models.Model):
    _inherit = 'project.task'

    # This Method Used to Restrict user to move task for specific stage if user
    # have no 'Billing Administrator' Rights.
    @api.model
    def create(self, vals):
        if (self.env.user.id != SUPERUSER_ID) and vals.get('stage_id', False):
            ir_model_data = self.env['ir.model.data']
            billing_group_id = ir_model_data.get_object_reference(
                'account', 'group_account_manager')[1]
            stageId = self.env['project.task.type'].browse(vals['stage_id'])
            if (stageId.move_allow and
                    (billing_group_id not in self.env.user.groups_id.ids)):
                raise UserError(_('You Are Not Allowed To Move This Task'))
        return super(ProjectTask, self).create(vals)


    # This Method Used to Restrict user to move task for specific stage if user
    # have no 'Billing Administrator' Rights.
    def write(self, vals):
        if (self.env.user.id != SUPERUSER_ID) and vals.get('stage_id', False):
            ir_model_data = self.env['ir.model.data']
            billing_group_id = ir_model_data.get_object_reference(
                'account', 'group_account_manager')[1]
            stageId = self.env['project.task.type'].browse(vals['stage_id'])
            if (stageId.move_allow and
                    (billing_group_id not in self.env.user.groups_id.ids)):
                raise UserError(_('You Are Not Allowed To Move This Task'))
        return super(ProjectTask, self).write(vals)
