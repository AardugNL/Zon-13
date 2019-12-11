# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Caret IT Solutions Pvt. Ltd. (Website: www.caretit.com).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

from odoo import api, fields, models, _


class ResCompany(models.Model):
    _inherit = "res.company"

    report_header_one = fields.Binary("Header One")
    report_header_two = fields.Binary("Header Two")
    report_header_three = fields.Binary("Header Three")
    report_header_four = fields.Binary("Header four") 
    report_footer_one = fields.Binary("Footer One")
    report_footer_two = fields.Binary("Footer Two")
    report_footer_three = fields.Binary("Footer Three")
    report_footer_four = fields.Binary("Footer Four")
    name_report_header_one = fields.Char('File Name of Header One')
    name_report_header_two = fields.Char('File Name of Header Two')
    name_report_header_three = fields.Char('File Name of Header Three')
    name_report_header_four = fields.Char('File Name of Header Four')
    name_report_footer_one = fields.Char('File Name of Footer One')
    name_report_footer_two = fields.Char('File Name of Footer Two')
    name_report_footer_three = fields.Char('File Name of Footer Three')
    name_report_footer_four = fields.Char('File Name of Footer Four')
    
    # not use more , but still write these fields for avoid existing data error    
    header_image = fields.Binary("Header Image", attachment=True)
    footer_blank_image = fields.Binary("Footer Image", attachment=True)
    file_name_footer_blank = fields.Char('File Name Footer')
    file_name_header = fields.Char('File Name Header')
    for_all_report = fields.Boolean("Use images for all report")

    @api.onchange('for_all_report')
    def onchange_for_all_report(self):
        if self.for_all_report:
            ir_model_data = self.env['ir.model.data']
            self.paperformat_id = ir_model_data.get_object_reference('custom_header_footer', 'paperformat_custom_header_footer')[1]
        else:
            paperformat_us = self.env.ref('base.paperformat_us', False)
            if paperformat_us and paperformat_us.id or False:
                self.paperformat_id = paperformat_us and paperformat_us.id or False
