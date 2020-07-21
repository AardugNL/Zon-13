# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

import datetime
import pytz    # $ pip install pytz
from odoo import models, fields, api, tools


DTFORMAT = tools.DEFAULT_SERVER_DATETIME_FORMAT


class Task(models.Model):
    _inherit = 'project.task'

    @api.model
    def getClientTz(self):
        """Return timezone from _context or env otherwise utc."""
        return self._context.get('tz') or self.env.user.tz or 'utc'

    @api.model
    def getClientPyTz(self):
        """Return getClientTz() as pytz."""
        return pytz.timezone(self.getClientTz())

    @api.model
    def getClientAsUTC(self, _date):
        """Return given time as utc based on timezone from environment."""
        return self.getClientPyTz().localize(_date).astimezone(pytz.utc)

    def clientEight(self):
        eightAM = datetime.datetime.combine(
            datetime.datetime.now().date(), datetime.time(8))
        return self.getClientAsUTC(eightAM).strftime(DTFORMAT)

    def clientSeventeen(self):
        fivePM = datetime.datetime.combine(
            datetime.datetime.now().date(), datetime.time(17))
        return self.getClientAsUTC(fivePM).strftime(DTFORMAT)

    resource_ids = fields.Many2many(
        'resource.resource', string='Team Members', track_visibility='always')
    notes_for_email = fields.Text()
    date_start = fields.Datetime(string="Starting Date", default=clientEight)
    date_end = fields.Datetime(string="Ending Date", default=clientSeventeen)
    resource_name = fields.Char("Name", compute='_computeResourceName')
    partner_shipping_id = fields.Many2one(
        'res.partner', string='Delivery Address')
    # duration = fields.Integer(
    #     'Duration', compute='_compute_duration', readonly=True, store=True)
    date_finished = fields.Datetime('Done Date')

    # @api.depends('date_end', 'date_start')s
    # def _compute_duration(self):
    #     for task in self:
    #         duration = 0.0
    #         if task.date_start and task.date_end:
    #             duration = (
    #                 fields.Datetime.from_string(task.date_end) -
    #                 fields.Datetime.from_string(task.date_start)
    #             ).total_seconds()
    #         task.duration = duration

    @api.depends('resource_ids')
    def _computeResourceName(self):
        for rec in self:
            name = [x.name for x in rec.resource_ids]
            if name:
                rec.resource_name = ', '.join(name)
            else:
                rec.resource_name = ''

    # def filterResourceStartEnd(self, d_frm_obj, d_to_obj):
    #     d_to_obj += datetime.timedelta(days=1)
    #     cr = self.env.cr
    #     cr.execute("""
    #         SELECT id FROM resource_start_end
    #         WHERE (start_date, end_date) OVERLAPS ('%s', '%s')""" % (
    #         d_frm_obj.date(), d_to_obj.date()))
    #     return cr.fetchall()
