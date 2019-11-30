from odoo import models, fields, api, tools

class ProductTemplate(models.Model):
    _inherit = "product.template"

    ec_watt_piek = fields.Float(string="EC Watt Piek")
    ec_iso = fields.Float(string="EC ISO")


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _order_watt_piek_and_iso(self):
        """ Calculates Sub total for watt piek and iso"""
        for order in self:
            total_ec_watt_piek = 0.0
            total_ec_order_iso = 0.0
            for line in order.order_line:
                total_ec_watt_piek += line.total_ec_watt_piek
                total_ec_order_iso += line.total_ec_iso
            order.ec_order_watt_piek = total_ec_watt_piek
            order.ec_order_iso = total_ec_order_iso

    ec_order_watt_piek = fields.Monetary(compute='_order_watt_piek_and_iso', string="EC Order Watt Piek")
    ec_order_iso = fields.Monetary(compute='_order_watt_piek_and_iso', string="EC Order ISO")


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.depends('product_id','ec_watt_piek', 'ec_iso', 'product_uom_qty')
    def _sub_total_watt_piek_and_iso(self):
        """ Calculates Sub total for watt piek and iso"""
        for line in self:
            if line.product_id and line.product_id.ec_watt_piek > 0.0 or line.product_id.ec_iso > 0.0:
                line.total_ec_watt_piek = line.product_uom_qty * line.ec_watt_piek
                line.total_ec_iso = line.product_uom_qty * line.ec_iso
            else:
                line.total_ec_iso = 0.0
                line.total_ec_watt_piek = 0.0

    ec_watt_piek = fields.Float(related="product_id.product_tmpl_id.ec_watt_piek",string="EC Watt Piek")
    ec_iso = fields.Float(related="product_id.product_tmpl_id.ec_iso",string="EC ISO")
    total_ec_watt_piek = fields.Float(compute='_sub_total_watt_piek_and_iso', string="Total EC Watt Piek",store=True)
    total_ec_iso = fields.Float(compute='_sub_total_watt_piek_and_iso', string="Total EC ISO",store=True)
