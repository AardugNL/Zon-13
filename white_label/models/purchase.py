# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Caret IT Solutions Pvt. Ltd. (Website: www.caretit.com).           # 
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

from odoo import models, fields, api

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    XA_box_quantity  = fields.Float('Box Quantity', compute='compute_purchase_box_at_date', store=True)
    XA_box_square_meter = fields.Float('Box Square Meter', compute='compute_purchase_box_at_date', store=True)
    XA_box_weight = fields.Float('Box Weight', compute='compute_purchase_box_at_date', store=True)
    XA_pallet_boxes = fields.Float('Pallet Boxes', compute='compute_purchase_box_at_date', store=True)
    XA_pallet_square_meter = fields.Float('Pallet Square Meter', compute='compute_purchase_box_at_date', store=True)
    XA_pallet_weight = fields.Float('Pallet Weight', compute='compute_purchase_box_at_date', store=True)


    @api.depends('product_id')
    def compute_purchase_box_at_date(self):
        for record in self:
            record.XA_box_quantity = record.product_id.XA_box_quantity
            record.XA_box_square_meter = record.product_id.XA_box_square_meter
            record.XA_box_weight = record.product_id.XA_box_weight
            record.XA_pallet_boxes = record.product_id.XA_pallet_boxes
            record.XA_pallet_square_meter = record.product_id.XA_pallet_square_meter
            record.XA_pallet_weight = record.product_id.XA_pallet_weight