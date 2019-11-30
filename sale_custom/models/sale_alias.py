# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Caret IT Solutions Pvt. Ltd. (Website: www.caretit.com).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

from odoo import api, fields, models, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    sale_alias = fields.Many2one('mail.alias', 'Alias', readonly=True)
    attachment_ids = fields.One2many('ir.attachment', 'order_id', string='Attachments')

    @api.model
    def create(self,vals):
        res = super(SaleOrder,self).create(vals)
        MailAlias = self.env['mail.alias']
        ir_model = self.env['ir.model'].search([('model','=','sale.order')])
        alias_id = MailAlias.create({
                    'alias_name':res.name,
                    'alias_model_id' : ir_model.id,
                    'alias_defaults' : {'order_id' : res.id},
                    })
        res.sale_alias = alias_id.id
        return res

    @api.model
    def message_new(self, msg, custom_values=None):
        if custom_values is None:
            custom_values = {}
        order = custom_values.get('order_id')
        if order:
            orderId = self.env['sale.order'].browse(order)
            return orderId
        else:
            return super(SaleOrder, self).message_new(msg, custom_values=custom_values)

    @api.returns('mail.message', lambda value: value.id)
    def message_post(self, subtype=None, **kwargs):
        self.ensure_one()
        if kwargs.get('message_type') == 'email':
            subtype = 'mail.mt_note'
        return super(SaleOrder, self).message_post(subtype=subtype, **kwargs)


class Task(models.Model):
    _inherit = 'project.task'

    task_alias = fields.Many2one('mail.alias', 'Alias', readonly=True)
    attachment_ids = fields.One2many('ir.attachment', 'task_id', string='Attachments')

    @api.model
    def create(self,vals):
        res = super(Task,self).create(vals)
        MailAlias = self.env['mail.alias']
        ir_model = self.env['ir.model'].search([('model','=','project.task')])
        alias_id = MailAlias.create({
                    'alias_name':res.code,
                    'alias_model_id' : ir_model.id,
                    'alias_defaults' : {'task_id' : res.id},
                    'alias_user_id': res.user_id.id
                    })
        res.task_alias = alias_id.id
        return res

    @api.model
    def message_new(self, msg, custom_values=None):
        if custom_values is None:
            custom_values = {}
        task = custom_values.get('task_id', None)
        if task:
            taskId = self.browse(task)
            return taskId
        else:
            return super(Task, self).message_new(msg, custom_values=custom_values)

    @api.returns('mail.message', lambda value: value.id)
    def message_post(self, subtype=None, **kwargs):
        self.ensure_one()
        if kwargs.get('message_type') == 'email':
            subtype = 'mail.mt_note'
        return super(Task, self).message_post(subtype=subtype, **kwargs)


class Lead(models.Model):
    _inherit = 'crm.lead'

    opp_alias = fields.Many2one('mail.alias', 'Alias', readonly=True)
    attachment_ids = fields.One2many('ir.attachment', 'lead_id', string='Attachments')

    @api.model
    def create(self,vals):
        res = super(Lead,self).create(vals)
        MailAlias = self.env['mail.alias']
        ir_model = self.env['ir.model'].search([('model','=','crm.lead')])
        alias_id = MailAlias.create({
                    'alias_name':res.code,
                    'alias_model_id' : ir_model.id,
                    'alias_defaults' : {'lead_id' : res.id},
                    'alias_user_id': res.user_id.id
                    })
        res.opp_alias = alias_id.id
        return res

    @api.model
    def message_new(self, msg, custom_values=None):
        if custom_values is None:
            custom_values = {}
        lead = custom_values.get('lead_id', None)
        if lead:
            leadId = self.browse(lead)
            return leadId
        else:
            return super(Lead, self).message_new(msg, custom_values=custom_values)

    @api.returns('mail.message', lambda value: value.id)
    def message_post(self, subtype=None, **kwargs):
        self.ensure_one()
        if kwargs.get('message_type') == 'email' and self.type == 'opportunity':
            subtype = 'mail.mt_note'
        return super(Lead, self).message_post(subtype=subtype, **kwargs)


class ProjectFormulier(models.Model):
    _inherit = 'question.formulier'

    formulier_alias = fields.Many2one('mail.alias', 'Alias', readonly=True)
    attachment_ids = fields.One2many('ir.attachment', 'formulier_id', string='Attachments')

    @api.model
    def create(self,vals):
        res = super(ProjectFormulier,self).create(vals)
        MailAlias = self.env['mail.alias']
        ir_model = self.env['ir.model'].search([('model','=','question.formulier')])
        alias_id = MailAlias.create({
                    'alias_name': res.code,
                    'alias_model_id' : ir_model.id,
                    'alias_defaults' : {'formulier_id' : res.id},
                    })
        res.formulier_alias = alias_id.id
        return res

    @api.model
    def message_new(self, msg, custom_values=None):
        if custom_values is None:
            custom_values = {}
        record = custom_values.get('formulier_id')
        if record:
            orderId = self.env['question.formulier'].browse(record)
            return orderId
        else:
            return super(ProjectFormulier, self).message_new(msg, custom_values=custom_values)

    @api.returns('mail.message', lambda value: value.id)
    def message_post(self, subtype=None, **kwargs):
        self.ensure_one()
        if kwargs.get('message_type') == 'email':
            subtype = 'mail.mt_note'
        return super(ProjectFormulier, self).message_post(subtype=subtype, **kwargs)


class Attachments(models.Model):
    _inherit = 'ir.attachment'

    task_id = fields.Many2one('project.task', string="Task")
    order_id = fields.Many2one('sale.order', string="Sale Order")
    lead_id = fields.Many2one('crm.lead', string="Opportunity")
    formulier_id = fields.Many2one('question.formulier', string="Project Formulier")

    @api.model
    def create(self,vals):
        res = super(Attachments,self).create(vals)
        if res.res_model == 'project.task':
            taskId = self.env['project.task'].search([
                    ('id', '=', res.res_id)], limit=1)
            if taskId:
                taskId.attachment_ids = [(4, res.id)]
        if res.res_model == 'sale.order':
            orderId = self.env['sale.order'].search([
                    ('id', '=', res.res_id)], limit=1)
            if orderId:
                orderId.attachment_ids = [(4,res.id)]
        if res.res_model == 'crm.lead':
            leadId = self.env['crm.lead'].search([
                    ('id', '=', res.res_id)], limit=1)
            if leadId:
                leadId.attachment_ids = [(4,res.id)]
        if res.res_model == 'question.formulier':
            formulierId = self.env['question.formulier'].search([
                    ('id', '=', res.res_id)], limit=1)
            if formulierId:
                formulierId.attachment_ids = [(4,res.id)]
        return res
