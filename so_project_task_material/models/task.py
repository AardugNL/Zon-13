# Part of Caret IT Solutions Pvt. Ltd. (Website: www.caretit.com).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class ProjectTask(models.Model):
    _inherit = 'project.task'

    planned_material_ids = fields.One2many(
        'planned.material.line', 'task_id', string='planned Tasks')
    consumed_material_ids = fields.One2many(
        'consumed.material.line', 'task_id', string='consumed Tasks')

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=None):
        context = self._context or {}
        if 'return_order_line_id' in context.keys():
            if context.get('return_order_line_id') and type(context.get('return_order_line_id')) == int:
                line_id = self.env['sale.order.line'].browse(context.get('return_order_line_id'))
                if line_id and line_id.order_id:
                    args += [('id', 'in', line_id.order_id.tasks_ids.ids)]
                else:
                    args += [('id', 'in', [])]
            else:
                raise UserError('Please first save record!')
        return super(ProjectTask, self).name_search(name, args, operator=operator, limit=limit)

    def print_task_report(self):
        return self.env.ref('so_project_task_material.report_task').report_action(self)

class PlannedMaterialLine(models.Model):
    _name = 'planned.material.line'
    _description = 'Planned Material'

    name = fields.Text(string='Description', required=True)
    product_id = fields.Many2one('product.product', string='Product',
        domain=[('sale_ok', '=', True)], change_default=True, 
        ondelete='restrict', required=True)
    product_uom = fields.Many2one('uom.uom', string='Unit of Measure',
        required=True)
    sale_line_id = fields.Many2one('sale.order.line', string='SO Line')
    planned_qty = fields.Float(string='Planned Qty',
        digits='Product Unit of Measure',
        required=True, default=1.0)
    task_id = fields.Many2one('project.task',
        string='Project task',
        change_default=True)

    @api.onchange('product_id')
    def product_id_change(self):
        if not self.product_id:
            return {'domain': {'product_uom': []}}

        vals = {}
        domain = {'product_uom': [
        ('category_id', '=', self.product_id.uom_id.category_id.id)]}
        if not self.product_uom or (self.product_id.uom_id.id != self.product_uom.id):
            vals['product_uom'] = self.product_id.uom_id
            vals['planned_qty'] = 1.0

        result = {'domain': domain}

        name = self.product_id.name_get()[0][1]
        if self.product_id.description_sale:
            name += '\n' + self.product_id.description_sale
        vals['name'] = name
        self.update(vals)
        return result

    @api.onchange('planned_qty')
    def onchange_planned(self):
        rec = self.env['consumed.material.line'].search('sale_line_id', '=', self.sale_line_id.id)
        if rec:
            rec.planned_qty = self.planned_qty


class ConsumedMaterialLine(models.Model):
    _name = 'consumed.material.line'
    _description = 'Consumed Material'

    name = fields.Text(string='Description', required=True)
    product_id = fields.Many2one('product.product', string='Product',
        domain=[('sale_ok', '=', True)], change_default=True, 
        ondelete='restrict', required=True)
    consumed_qty = fields.Float(string='Consumed Qty',
        digits='Product Unit of Measure',
        required=True, default=1.0)
    product_uom = fields.Many2one('uom.uom', string='Unit of Measure',
        required=True)
    sale_line_id = fields.Many2one('sale.order.line', string='SO Line')
    planned_qty = fields.Float(string='Planned Qty',
        digits='Product Unit of Measure',
        required=True, default=1.0)
    sale_id = fields.Many2one('sale.order', string='Sale Order')
    task_id = fields.Many2one('project.task',
        string='Project task',
        change_default=True)
    create_from_button = fields.Boolean(default=False)

    @api.onchange('product_id')
    def product_id_change(self):
        if not self.product_id:
            return {'domain': {'product_uom': []}}

        vals = {}
        domain = {'product_uom': [
        ('category_id', '=', self.product_id.uom_id.category_id.id)]}
        if not self.product_uom or (self.product_id.uom_id.id != self.product_uom.id):
            vals['product_uom'] = self.product_id.uom_id.id
            vals['planned_qty'] = 1.0
            vals['consumed_qty'] = 1.0

        result = {'domain': domain}

        name = self.product_id.name_get()[0][1]
        if self.product_id.description_sale:
            name += '\n' + self.product_id.description_sale
        vals['name'] = name
        self.update(vals)
        return result

    @api.model
    def create(self, vals):
        if vals.get('product_id'):
            SaleOrderLine = self.env['sale.order.line']
            product_id = self.env['product.product'].browse(vals.get('product_id'))
            bom = self.env['mrp.bom'].sudo()._bom_find(product=product_id,
                                                        company_id=self.env.user.company_id.id)
            if not bom or bom.type != 'phantom':
                consumed_qty = vals.get('consumed_qty')
                vals.update({'consumed_qty': 0.0})
                res = super(ConsumedMaterialLine,self).create(vals)
                if not res.create_from_button:
                    solId = SaleOrderLine.create({
                        'product_id': res.product_id.id,
                        'name': res.name,
                        'product_uom_qty': res.consumed_qty or res.planned_qty,
                        'product_uom': res.product_uom.id,
                        'order_id': res.sale_id.id,
                        'task_id': res.task_id.id,
                        'planned_qty': res.planned_qty,
                        })
                    res.sale_line_id = solId.id
                    res.write({'consumed_qty': consumed_qty})
                return res
            if bom and bom.bom_line_ids:
                planned_qty = vals.get('planned_qty') or 1.0
                consumed_qty = vals.get('consumed_qty')
                if not vals.get('create_from_button'):
                    solId = SaleOrderLine.create({
                        'product_id': vals.get('product_id'),
                        'name': vals.get('name'),
                        'product_uom_qty': vals.get('consumed_qty') or vals.get('planned_qty'),
                        'product_uom': vals.get('product_uom'),
                        'order_id': vals.get('sale_id'),
                        'task_id': vals.get('task_id'),
                        'planned_qty': vals.get('planned_qty'),
                        })
                    vals.update({'sale_line_id': solId.id})
                for bom_component in bom.bom_line_ids:
                    new_vals = vals
                    old_name = vals.get('name') or ''
                    new_vals.update({'product_id': bom_component.product_id.id,
                                    'name': bom_component.product_id.name + ' ('+old_name+')',
                                    'planned_qty': planned_qty*bom_component.product_qty})
                    vals.update({'consumed_qty': 0.0})
                    res = super(ConsumedMaterialLine,self).create(new_vals)
                    res.write({'consumed_qty': consumed_qty})
                return res
        return super(ConsumedMaterialLine,self).create(vals)

    def picking_line_update(self, picking, r_qty):
        qty = r_qty
        for products in picking.move_ids_without_package:
            try:
                if products.product_id.id == self.product_id.id:
                    if products.sale_line_id.id != self.sale_line_id.id:
                        before_qty = products.quantity_done
                        new_qty = before_qty + qty
                        if products.product_qty != products.quantity_done and new_qty >= products.product_qty:
                            products.quantity_done = products.product_qty
                            qty = abs(new_qty - products.product_qty)
                    if products.sale_line_id.id == self.sale_line_id.id:
                        products.quantity_done = qty + products.quantity_done
                        qty = qty - qty
                if qty <= 0:
                    break
            except Exception as e:
                pass
        picking.button_validate()

    def picking_update(self, done_qty):
        Picking = self.env['stock.picking']
        stock_picking_ids = Picking.search([("origin", '=', self.sale_line_id.order_id.name),
                                            ('state', 'not in', ('done', 'cancel'))])
        for picking in stock_picking_ids:
            if picking.state == 'draft':
                picking.action_confirm()
                self.picking_line_update(picking,done_qty)
            elif picking.state == 'waiting':
                picking.action_assign()
                self.picking_line_update(picking,done_qty)
            elif picking.state == 'confirmed':
                picking.action_assign()
                self.picking_line_update(picking,done_qty)
            elif picking.state == 'partially_available':
                self.picking_line_update(picking,done_qty)
            elif picking.state == 'assigned':
                self.picking_line_update(picking,done_qty)

    @api.model
    def write(self, vals):
        SaleOrderLine = self.env['sale.order.line']
        if self.sale_line_id:
            if vals.get('name'):
                self.sale_line_id.name = vals.get('name')
            if vals.get('product_id'):
                self.sale_line_id.product_id = vals.get('product_id')
            if vals.get('consumed_qty'):
                consumed_qty = vals.get('consumed_qty')
                bom_prod_qty = 0.0
                for line in self.sale_id.order_line:
                    if line.product_id.id != self.product_id.id:
                        bom = self.env['mrp.bom'].sudo()._bom_find(product=line.product_id,
                                                                    company_id=self.env.user.company_id.id)
                        if bom and bom.type == 'phantom':
                            for bom_prod in bom.bom_line_ids:
                                if bom_prod.product_id.id == self.product_id.id:
                                    bom_prod_qty = bom_prod_qty + (bom_prod.product_qty*line.product_uom_qty)
                new_qty = consumed_qty - bom_prod_qty
                done_qty = consumed_qty - self.consumed_qty
                if consumed_qty > self.planned_qty:# get difference between planned qty and consumed if greater consumed then write in orderd qty
                    if self.product_id.id == self.sale_line_id.product_id.id:
                        if new_qty > 0.0:
                            self.sale_line_id.product_uom_qty = new_qty
                    if self.sale_line_id.product_id.id != self.product_id.id:
                        if new_qty > 0.0:
                            solId = SaleOrderLine.create({
                                    'product_id': self.product_id.id,
                                    'name': self.name,
                                    'product_uom_qty': new_qty,
                                    'product_uom': self.product_uom.id,
                                    'order_id': self.sale_id.id,
                                    'task_id': self.task_id.id,
                                    'planned_qty': new_qty,
                                    })
                            self.sale_line_id = solId.id
                    self.picking_update(done_qty)
                elif consumed_qty < self.consumed_qty:# if it is decrease then error
                    raise UserError('You can not decrease done consumed qty')
                elif consumed_qty > self.consumed_qty:# if consumed increase then done that qty in delivery
                    self.picking_update(done_qty)

        return super(ConsumedMaterialLine, self).write(vals)

