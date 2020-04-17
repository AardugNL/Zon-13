# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################


from odoo import api, fields, models, _


class ProductTemplateInh(models.Model):
    _inherit = 'product.template'

    task_material = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No')],
        string='Task Material')