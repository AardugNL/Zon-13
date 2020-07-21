# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

import pytz    # $ pip install pytz
# import datetime
from odoo import models, fields, api
from odoo.http import request
from odoo.exceptions import ValidationError


# def startOfDay(date_):
#     if isinstance(date_, datetime.datetime):
#         return date_.replace(
#             hour=00, minute=00, second=00, microsecond=00)
#     else:
#         return date_


# def endOfDay(date_):
#     if isinstance(date_, datetime.datetime):
#         return date_.replace(
#             hour=23, minute=59, second=59, microsecond=999999)
#     else:
#         return date_


class Resource(models.Model):
    _inherit = 'resource.resource'

    @api.model
    def getTzTimeForThisTime(self, dtime):
        tzone = pytz.timezone(request.context.get('tz', 'utc') or 'utc')
        if dtime.tzinfo:
            return dtime.astimezone(tzone)
        return dtime.replace(tzinfo=pytz.timezone('utc')).astimezone(tzone)

    @api.constrains('start_end_ids')
    def dateCheck(self):
        for record in self.start_end_ids:
            if record.start_date > record.end_date:
                raise ValidationError('Error! Start date must be lower than '
                                      'End date or same as End date')

    resource_image = fields.Binary('Photo', attachment=True)
    # duration = fields.Char(string='Duration')
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    str_category = fields.Char(compute='getCategoryNames')
    start_end_ids = fields.One2many(
        'resource.start_end', 'resource_id', string='Start End Date')
    employee_id = fields.Many2one('hr.employee', string='Employee')
    category_ids = fields.Many2many(
        'hr.employee.category', related='employee_id.category_ids',
        string='Tags')

    def getCategoryNames(self):
        for each in self:
            each.str_category = ', '.join([x.name for x in each.category_ids])

    # def kanban_done(self):
    #     return {'type': 'ir.actions.act_window_close', 'auto_refresh': '1'}

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        context = self._context or {}
        if context.get('res_task_id'):
            task = self.env['project.task'].browse(context.get('res_task_id'))
            args += [('id', 'in', [t.id for t in task.resource_ids])]
        return super(Resource, self).name_search(
            name, args=args, operator=operator, limit=limit)

    @api.model
    def create(self, vals):
        result = super(Resource, self).create(vals)
        if result.user_id and result.user_id.employee_ids:
            result.employee_id = result.user_id.employee_ids[0].id
        return result

    def write(self, vals, context=None):
        if vals.get('user_id'):
            user = self.user_id.browse(vals.get('user_id'))
            if user.employee_ids:
                vals['employee_id'] = user.employee_ids[0].id
            else: vals['employee_id'] = False
        return super(Resource, self).write(vals)


class CalendarEvent(models.Model):
    _inherit = 'calendar.event'

    resource_id = fields.Many2one('resource.resource', string="Resource")
    partner_shipping_id = fields.Many2one(
        'res.partner', string='Delivery Address')


class ResourceStartEnd(models.Model):
    _name = 'resource.start_end'
    _description = "Resource Start End Date"

    resource_id = fields.Many2one(
        'resource.resource', string='Resource', required=True)
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End date')


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    @api.model
    def create(self, vals):
        result = super(HrEmployee, self).create(vals)
        result.resource_id.employee_id = result.id
        return result
