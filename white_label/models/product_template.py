# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Caret IT Solutions Pvt. Ltd. (Website: www.caretit.com).           # 
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    XA_white_label_description = fields.Text(
        'White Label Description')
    XA_white_label_sale_price = fields.Float(
        'White Label Sales Price')
    XA_box_quantity = fields.Float('Box Quantity')
    XA_box_square_meter = fields.Float('Box Square Meter')
    XA_box_weight = fields.Float('Box Weight')
    XA_pallet_boxes = fields.Float('Pallet Boxes')
    XA_pallet_square_meter = fields.Float('Pallet Square Meter')
    XA_pallet_weight = fields.Float('Pallet Weight')


    @api.model
    def create(self, values):
        record = super(ProductTemplate, self).create(values)
        if not record.XA_white_label_description and record.XA_white_label_sale_price == 0.00:
            record.XA_white_label_description = record.description_sale 
            record.XA_white_label_sale_price = record.list_price
        return record