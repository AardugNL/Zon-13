# Part of Caret IT Solutions Pvt. Ltd. (Website: www.caretit.com).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

from odoo import api, fields, models, _
from odoo.tools import float_compare
from odoo.exceptions import UserError

class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    state = fields.Selection(selection_add=[
        ('material_to_task', 'Material To Task'),],
        string='Status', readonly=True, copy=False,
        index=True, track_visibility='onchange', default='draft')

    def material_to_task(self):
        plannedObj = self.env['planned.material.line']
        consumedObj = self.env['consumed.material.line']
        for line in self.order_line:
            if not line.material_to_task:
                if line.task_id:
                    plannedObj.create({
                        'product_id': line.product_id.id,
                        'sale_line_id': line.id,
                        'planned_qty': line.product_uom_qty,
                        'name': line.name,
                        'product_uom': line.product_uom.id,
                        'task_id': line.task_id.id,
                        })
                    consumedObj.create({
                        'product_id': line.product_id.id,
                        'sale_line_id': line.id,
                        'planned_qty': line.product_uom_qty,
                        'consumed_qty': 0.00,
                        'name': line.name,
                        'product_uom': line.product_uom.id,
                        'sale_id': line.order_id.id,
                        'task_id': line.task_id.id,
                        'create_from_button': True,
                        })
                line.material_to_task = True
                line.order_id.state = 'material_to_task'


class SaleOrderLineInh(models.Model):
    _inherit = 'sale.order.line'

    tm = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No')],
        string='TM')
    material_to_task = fields.Boolean(string='Material To Task')
    planned_qty = fields.Float(string='Planned Qty',
        digits='Product Unit of Measure',
        required=True, default=1.0)

    def _action_launch_stock_rule(self, previous_product_uom_qty=False):
        """
        Launch procurement group run method with required/custom fields genrated by a
        sale order line. procurement group will launch '_run_pull', '_run_buy' or '_run_manufacture'
        depending on the sale order line product rule.
        """
        precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')
        procurements = []
        for line in self:
            if line.state not in ['sale', 'material_to_task'] or not line.product_id.type in ('consu','product'):
                continue
            qty = line._get_qty_procurement(previous_product_uom_qty)
            if float_compare(qty, line.product_uom_qty, precision_digits=precision) >= 0:
                continue

            group_id = line._get_procurement_group()
            if not group_id:
                group_id = self.env['procurement.group'].create(line._prepare_procurement_group_vals())
                line.order_id.procurement_group_id = group_id
            else:
                # In case the procurement group is already created and the order was
                # cancelled, we need to update certain values of the group.
                updated_vals = {}
                if group_id.partner_id != line.order_id.partner_shipping_id:
                    updated_vals.update({'partner_id': line.order_id.partner_shipping_id.id})
                if group_id.move_type != line.order_id.picking_policy:
                    updated_vals.update({'move_type': line.order_id.picking_policy})
                if updated_vals:
                    group_id.write(updated_vals)

            values = line._prepare_procurement_values(group_id=group_id)
            product_qty = line.product_uom_qty - qty

            line_uom = line.product_uom
            quant_uom = line.product_id.uom_id
            product_qty, procurement_uom = line_uom._adjust_uom_quantities(product_qty, quant_uom)
            procurements.append(self.env['procurement.group'].Procurement(
                line.product_id, product_qty, procurement_uom,
                line.order_id.partner_shipping_id.property_stock_customer,
                line.name, line.order_id.name, line.order_id.company_id, values))
        if procurements:
            self.env['procurement.group'].run(procurements)
        return True

    @api.model_create_multi
    def create(self, vals_list):
        for values in vals_list:
            if values.get('display_type', self.default_get(['display_type'])['display_type']):
                values.update(product_id=False, price_unit=0, product_uom_qty=0, product_uom=False, customer_lead=0)
            values.update(self._prepare_add_missing_fields(values))
            values.update({'planned_qty': values.get('product_uom_qty')})
        order_line = super(SaleOrderLineInh, self).create(vals_list)
        for line in order_line:
            if line.order_id:
                task_lin = self.search([('order_id','=',line.order_id.id),
                            ('task_id','!=',False)],limit=1)
                lines = self.search([('order_id','=',line.order_id.id),
                            ('task_id','=',False)])
                if task_lin and lines:
                    for l in lines:
                        l.task_id = task_lin.task_id.id
            if line.product_id and line.order_id.state in ['sale', 'material_to_task']:
                line._action_launch_stock_rule()
                msg = _("Extra line with %s ") % (line.product_id.display_name,)
                line.order_id.message_post(body=msg)
                # create an analytic account if at least an expense product
                if line.product_id.expense_policy not in [False, 'no'] and not self.order_id.analytic_account_id:
                    self.order_id._create_analytic_account()

            plannedObj = self.env['planned.material.line']
            consumedObj = self.env['consumed.material.line']
            if line.material_to_task == True:
                if line.task_id:
                    plannedObj.create({
                        'product_id': line.product_id.id,
                        'sale_line_id': line.id,
                        'planned_qty': line.product_uom_qty,
                        'name': line.name,
                        'product_uom': line.product_uom.id,
                        'task_id': line.task_id.id,
                        })
                    consumedObj.create({
                        'product_id': line.product_id.id,
                        'sale_line_id': line.id,
                        'planned_qty': line.product_uom_qty,
                        'consumed_qty': 0.00,
                        'name': line.name,
                        'product_uom': line.product_uom.id,
                        'sale_id': line.order_id.id,
                        'task_id': line.task_id.id,
                        'create_from_button': True,
                        })

        return order_line

    def write(self, values):
        lines = self.env['sale.order.line']
        if 'display_type' in values and self.filtered(lambda line: line.display_type != values.get('display_type')):
            raise UserError(_("You cannot change the type of a sale order line. Instead you should delete the current line and create a new line of the proper type."))
        if 'product_uom_qty' in values:
            precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')
            lines = self.filtered(
                lambda r: r.state in ['sale', 'material_to_task'] and not r.is_expense and float_compare(r.product_uom_qty, values['product_uom_qty'], precision_digits=precision) == -1)
            self.filtered(
                lambda r: r.state in ['sale', 'material_to_task'] and float_compare(
                    r.product_uom_qty, values['product_uom_qty'], precision_digits=precision) != 0
                )._update_line_quantity(values)
            if self.state != 'material_to_task':
                for planned_material_id in self.task_id.planned_material_ids:
                    if planned_material_id.sale_line_id.id == self.id:
                        planned_material_id.write({'planned_qty': values.get('product_uom_qty')}) #check if write from sale line then what
                        self.write({'planned_qty': values.get('product_uom_qty')}) #check if write from sale line then what

        # Prevent writing on a locked SO.
        protected_fields = self._get_protected_fields()
        if 'done' in self.mapped('order_id.state') and any(f in values.keys() for f in protected_fields):
            protected_fields_modified = list(set(protected_fields) & set(values.keys()))
            fields = self.env['ir.model.fields'].search([
                ('name', 'in', protected_fields_modified), ('model', '=', self._name)
            ])
            raise UserError(
                _('It is forbidden to modify the following fields in a locked order:\n%s')
                % '\n'.join(fields.mapped('field_description'))
            )

        result = super(SaleOrderLineInh, self).write(values)
        if values.get('task_id'):
            for l in self.order_id.order_line:
                if not l.task_id:
                    l.task_id = values.get('task_id')
        if lines:
            previous_product_uom_qty = {line.id: line.product_uom_qty for line in lines}
            lines._action_launch_stock_rule(previous_product_uom_qty)
        return result
