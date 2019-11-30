# -*- coding: utf-8 -*-
# Copyright 2016 Tecnativa <vicent.cubells@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


class ProjectFormulier(models.Model):
    _inherit = 'question.formulier'

    code = fields.Char(
        string='Formulier Number', required=True, default="/", readonly=True)

    _sql_constraints = [
        ('question_formulier_unique_code', 'UNIQUE (code)',
         _('The code must be unique!')),
    ]

    @api.model
    def create(self, vals):
        if vals.get('code', '/') == '/':
            vals['code'] = self.env['ir.sequence'].next_by_code('question.formulier')
        return super(ProjectFormulier, self).create(vals)

    def copy(self, default=None):
        if default is None:
            default = {}
        default['code'] = self.env['ir.sequence'].next_by_code('question.formulier')
        return super(ProjectFormulier, self).copy(default)
