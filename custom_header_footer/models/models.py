# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Caretit. (Website: www.caretit.com).                               #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

from odoo import api, fields, models, _


class ResPartner(models.Model):
    _inherit = "res.partner"

    trademark_type = fields.Selection([('company1', 'Company1'), ('company2', 'Company2'),
                                        ('company3', 'Company3') ,('company4', 'Company4')],
                                        default='company1', string='Trademark')

class CrmLead(models.Model):
    _inherit = "crm.lead"

    trademark_type = fields.Selection([('company1', 'Company1'), ('company2', 'Company2'),
                                        ('company3', 'Company3') ,('company4', 'Company4')],
                                        default='company1', string='Trademark')

class SaleOrder(models.Model):
    _inherit = "sale.order"

    trademark_type = fields.Selection([('company1', 'Company1'), ('company2', 'Company2'),
                                        ('company3', 'Company3') ,('company4', 'Company4')],
                                        related='opportunity_id.trademark_type', default='company1', string='Trademark')

    @api.model
    def _prepare_invoice(self):
        res = super(SaleOrder, self)._prepare_invoice()
        if res:
            res.update({'trademark_type': self.trademark_type or ''})
        return res


class AccountMove(models.Model):
    _inherit = "account.move"

    trademark_type = fields.Selection([('company1', 'Company1'), ('company2', 'Company2'),
                                        ('company3', 'Company3') ,('company4', 'Company4')],
                                        default='company1', string='Trademark')


class StockPicking(models.Model):
    _inherit = "stock.picking"

    trademark_type = fields.Selection([('company1', 'Company1'), ('company2', 'Company2'),
                                        ('company3', 'Company3') ,('company4', 'Company4')],
                                        default='company1', string='Trademark')
