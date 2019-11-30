# Part of Caret IT Solutions Pvt. Ltd. (Website: www.caretit.com).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

from odoo import api, fields, models, _
from odoo.exceptions import UserError

class ScrewPiles(models.Model):
    _name = 'screw.piles'
    _description = 'Screw Piles'

    name = fields.Char('Pole number')
    sawn_length = fields.Integer('Sawn Length')
    archived_torque = fields.Integer('Archived Torque')
    add_work = fields.Text('Add Work')
    remarks = fields.Text('Remarks')
    image = fields.Binary('Image', attachment=True)
    product_id = fields.Many2one('product.product', string='Product',
            domain=[('sale_ok', '=', True)], change_default=True, 
            ondelete='restrict', required=True)
    sale_line_id = fields.Many2one('sale.order.line', string='SO Line')
    sale_id = fields.Many2one('sale.order', string='Sale Order')
    question_frm_id = fields.Many2one(related='sale_id.question_frm_id',
        string='Project formulier')