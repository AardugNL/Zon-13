# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Caret IT Solutions Pvt. Ltd. (Website: www.caretit.com).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

from . import models
from odoo import api, SUPERUSER_ID

def create_code_equal_to_id(cr):
    """
    With this pre-init-hook we want to avoid error when creating the UNIQUE
    code constraint when the module is installed and before the post-init-hook
    is launched.
    """
    cr.execute('ALTER TABLE crm_lead '
               'ADD COLUMN code character varying;')
    cr.execute('UPDATE crm_lead '
               'SET code = id;')


def assign_old_sequences(cr, registry):
    """
    This post-init-hook will update all existing opportunity assigning them the
    corresponding sequence code.
    """
    
    env = api.Environment(cr, SUPERUSER_ID, dict())
    opp_obj = env['crm.lead']
    sequence_obj = env['ir.sequence']
    opps = opp_obj.search([], order="id")
    for opp_id in opps.ids:
        cr.execute('UPDATE crm_lead '
                   'SET code = %s '
                   'WHERE id = %s;',
                   (sequence_obj.next_by_code('crm.lead'), opp_id, ))
