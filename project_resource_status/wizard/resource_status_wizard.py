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


startOfDay = lambda date_: date_.replace(
    hour=00, minute=00, second=00, microsecond=00)
endOfDay = lambda date_: date_.replace(
    hour=23, minute=59, second=59, microsecond=999999)


class ResourceStatusWizard(models.Model):
    _name = "resource.status.wizard"
    _description = "Resource Status Wizard"

    start_date = fields.Datetime(string='Date From')
    end_date = fields.Datetime(string='Date To')

    def createResourceStatus(self):
        """create status for all resouces based on start date and end date"""
        resDailyStatusObj = self.env['resource.daily.status']
        timezone = resDailyStatusObj.getTimezone()

        if self.start_date and self.end_date:
            start = startOfDay(self.start_date)
            start = timezone.localize(start).astimezone(pytz.utc)
            end = endOfDay(self.end_date)
            end = timezone.localize(end).astimezone(pytz.utc)
            resDailyStatusObj.syncResourceForPeriod(start, end)
