# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
import re

class ProjectTask(models.Model):
    """ Project Task Tab """

    _inherit = "project.task"

    question_frm_id = fields.Many2one('question.formulier', string='Project Formulier')

    @api.model
    def create(self,vals):
        res = super(ProjectTask, self).create(vals)
        order_id = res.sale_order_id
        if order_id.question_frm_id:
            res.question_frm_id = order_id.question_frm_id.id
        return res

    def write(self,vals):
        res = super(ProjectTask, self).write(vals)
        if vals.get('sale_order_id'):
            sale_order_id = self.sale_order_id
            if sale_order_id.question_frm_id:
                self.question_frm_id = sale_order_id.question_frm_id.id
        return res
