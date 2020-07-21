# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

import datetime

def startOfDay(date_):
    '''replace timestamps for start date'''
    if isinstance(date_, datetime.datetime):
        return date_.replace(
            hour=00, minute=00, second=00, microsecond=00)
    else:
        return date_

def endOfDay(date_):
    '''replace timestamps for end date'''
    if isinstance(date_, datetime.datetime):
        return date_.replace(
            hour=23, minute=59, second=59, microsecond=999999)
    else:
        return date_
