# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

from odoo import api, fields, models, _

class CompanyInherit(models.Model):
    _inherit = "res.company"

    header_image = fields.Binary("Header Image")
    footer_blank_image = fields.Binary("Footer Image")
    file_name_footer_blank = fields.Char('File Name')
    file_name_header = fields.Char('File name')
    for_all_report = fields.Boolean("Use images for all report")

    @api.onchange('for_all_report')
    def onchange_for_all_report(self):
        if self.for_all_report:
            ir_model_data = self.env['ir.model.data']
            self.paperformat_id = ir_model_data.get_object_reference(
                'custom_header_footer', 'paperformat_custom_header_footer')[1]
        else:
            paperformat_us = self.env.ref('base.paperformat_us', False)
            if paperformat_us and paperformat_us.id or False:
                self.paperformat_id = paperformat_us and paperformat_us.id or False
