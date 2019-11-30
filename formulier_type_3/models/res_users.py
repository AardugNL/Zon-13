# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class ResUsers(models.Model):

    _inherit = "res.users"

    show_score = fields.Boolean('Show Score on PF')
