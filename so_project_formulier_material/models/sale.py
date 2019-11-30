# Part of Caret IT Solutions Pvt. Ltd. (Website: www.caretit.com).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

from odoo import api, fields, models, _
from odoo.exceptions import UserError

class SaleOrderLineInh(models.Model):
    _inherit = 'sale.order.line'

    question_frm_id = fields.Many2one(related='order_id.question_frm_id', string='Formulier Link')

    @api.model
    def create(self, vals):
        res = super(SaleOrderLineInh,self).create(vals)
        if res.question_frm_id:
            ScrewPiles = self.env['screw.piles'].sudo()
            bom = self.env['mrp.bom'].sudo()._bom_find(product=res.product_id,
                                                        company_id=res.company_id.id)
            if bom:
                for qty in range(1,int(res.product_uom_qty)+1):
                    piles_id = ScrewPiles.create({
                                        'name': res.name + ' Nr'+str(qty),
                                        'product_id': res.product_id.id,
                                        'sale_line_id': res.id,
                                        'sale_id': res.order_id.id,
                                        })
        return res