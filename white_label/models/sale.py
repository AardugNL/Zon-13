# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Caret IT Solutions Pvt. Ltd. (Website: www.caretit.com).           # 
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

from odoo import models, fields, api

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    XA_type_show = fields.Selection([
        ('brand', 'Brand'),
        ('whitelabel', 'White Label'),
    ], store=True, string='Type', default='brand')
    XA_box = fields.Float('Box')
    XA_box_quantity  = fields.Float('Box Quantity', compute='compute_box_at_date', store=True)
    XA_box_square_meter = fields.Float('Box Square Meter', compute='compute_box_at_date', store=True)
    XA_box_weight = fields.Float('Box Weight', compute='compute_box_at_date', store=True)
    XA_pallet_boxes = fields.Float('Pallet Boxes', compute='compute_box_at_date', store=True)
    XA_pallet_square_meter = fields.Float('Pallet Square Meter', compute='compute_box_at_date', store=True)
    XA_pallet_weight = fields.Float('Pallet Weight', compute='compute_box_at_date', store=True)


    @api.depends('product_id')
    def compute_box_at_date(self):
        for record in self:
            record.XA_box_quantity = record.product_id.XA_box_quantity
            record.XA_box_square_meter = record.product_id.XA_box_square_meter
            record.XA_box_weight = record.product_id.XA_box_weight
            record.XA_pallet_boxes = record.product_id.XA_pallet_boxes
            record.XA_pallet_square_meter = record.product_id.XA_pallet_square_meter
            record.XA_pallet_weight = record.product_id.XA_pallet_weight

    @api.onchange('product_uom_qty')
    def _compute_boxes(self):
        if self.product_id:
            for line in self:
                if line.product_id.XA_box_square_meter > 0.0:
                    line.XA_box = line.product_uom_qty / line.product_id.XA_box_square_meter

    @api.onchange('XA_box')
    def _compute_quantity(self):
        if self.product_id:
            for line in self:
                line.product_uom_qty = line.XA_box * line.product_id.XA_box_square_meter

    @api.onchange('XA_type_show')
    def product_type_change(self):
        if not self.XA_type_show or not self.product_id:
            self.price_unit = 0.0
            return
        if self.XA_type_show == 'whitelabel':
            self.name = self.product_id.XA_white_label_description
            self.price_unit = self.product_id.XA_white_label_sale_price
        else:
            self.name = self.get_sale_order_line_multiline_description_sale(self.product_id)
            self.price_unit = self.product_id.list_price
