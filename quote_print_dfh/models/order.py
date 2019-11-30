# -*- coding: utf-8 -*-

from odoo import api, fields, models

class sale_order_template_inherit(models.Model):
    _inherit = "sale.order.template"

    report_layout = fields.Selection(selection_add=[('dfh_layout', 'DFH Layout')],
                                    string='Report Layout')
