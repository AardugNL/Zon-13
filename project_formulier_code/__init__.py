# -*- coding: utf-8 -*-
# Copyright 2016 Tecnativa <vicent.cubells@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from . import models
from odoo import api, SUPERUSER_ID

def create_code_equal_to_id(cr):
    """
    With this pre-init-hook we want to avoid error when creating the UNIQUE
    code constraint when the module is installed and before the post-init-hook
    is launched.
    """
    cr.execute('ALTER TABLE question_formulier '
               'ADD COLUMN code character varying;')
    cr.execute('UPDATE question_formulier '
               'SET code = id;')


def assign_old_sequences(cr, registry):
    """
    This post-init-hook will update all existing formulier assigning them the
    corresponding sequence code.
    """
    env = api.Environment(cr, SUPERUSER_ID, dict())
    formulier_obj = env['question.formulier']
    sequence_obj = env['ir.sequence']
    formuliers = formulier_obj.search([], order="id")
    for formulier_id in formuliers.ids:
        cr.execute('UPDATE question_formulier '
                   'SET code = %s '
                   'WHERE id = %s;',
                   (sequence_obj.next_by_code('question.formulier'), formulier_id, ))
