# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Caret IT Solutions Pvt. Ltd. (Website: www.caretit.com).           # 
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

from odoo import api, fields, models, _


class PartnerSalutation(models.Model):
    _inherit = 'res.partner'

    firstname = fields.Char("First name")
    lastname = fields.Char("Last name")
    informal_salutation = fields.Selection([('hello','Hello'),
                                            ('best','Best')],
                                            string='Informal Salutation')
    formal_salutation = fields.Selection([('dear','Dear')],
                                        string='Formal Salutation')
    formal_partner_salutation = fields.Char(string='Formal Partner Salutation')
    informal_partner_salutation = fields.Char(string='Informal Partner Salutation')

    @api.onchange('informal_salutation', 'firstname')
    def _onchange_partner_salutation(self):
        if self.firstname and self.informal_salutation:
            informal_salutation = dict(self._fields['informal_salutation'].selection).get(self.informal_salutation)
            self.informal_partner_salutation = _(informal_salutation)+ ' ' + self.firstname
        else:
            self.informal_partner_salutation = False

    @api.onchange('formal_salutation', 'title', 'lastname')
    def _onchange_par_formal_salutation(self):
        if self.lastname and self.formal_salutation:
            nameContent = []
            formal_salutation = dict(self._fields['formal_salutation'].selection).get(self.formal_salutation)
            nameContent.append(_(formal_salutation))
            nameContent.append(self.title and self.title.name or '')
            nameContent.append(self.lastname or '')
            title = ' '.join([x for x in nameContent if x])
            self.formal_partner_salutation = title
        else:
            self.formal_partner_salutation = False


class CrmSalutation(models.Model):
    _inherit = 'crm.lead'

    firstname = fields.Char("First name")
    lastname = fields.Char("Last name")
    informal_salutation = fields.Selection([('hello','Hello'),
                                            ('best','Best')],
                                            string='Informal Salutation')
    formal_salutation = fields.Selection([('dear','Dear')],
                                        string='Formal Salutation')
    formal_salutation_result = fields.Char(string='Formal Partner Salutation')
    informal_salutation_result = fields.Char(string='Informal Partner Salutation')

    @api.onchange('informal_salutation','firstname')
    def _onchange_informal_salutation(self):
        contactName = []
        if self.firstname and self.informal_salutation:
            informal_salutation = dict(self._fields['informal_salutation'].selection).get(self.informal_salutation)
            self.informal_salutation_result = _(informal_salutation)+ ' ' + self.firstname
        else:
            self.informal_salutation_result = False
        contactName.append(self.firstname)
        contactName.append(self.lastname)
        fullname = ' '.join([x for x in contactName if x])
        if fullname:
            self.contact_name = fullname

    @api.onchange('formal_salutation', 'title', 'lastname')
    def _onchange_par_formal_salutation(self):
        contactName = []
        if self.lastname and self.formal_salutation:
            nameContent = []
            formal_salutation = dict(self._fields['formal_salutation'].selection).get(self.formal_salutation)
            nameContent.append(_(formal_salutation))
            nameContent.append(self.title and self.title.name)
            nameContent.append(self.lastname or '')
            titles = ' '.join([x for x in nameContent if x])
            self.formal_salutation_result = titles
        else:
            self.formal_salutation_result = False
        contactName.append(self.firstname)
        contactName.append(self.lastname)
        fullname = ' '.join([x for x in contactName if x])
        if fullname:
            self.contact_name = fullname

    @api.onchange('partner_id')
    def _onchange_crmpartner_salutation(self):
        self.formal_salutation_result = self.partner_id.formal_partner_salutation
        self.informal_salutation_result = self.partner_id.informal_partner_salutation
        self.firstname = self.partner_id.firstname
        self.lastname = self.partner_id.lastname
        self.formal_salutation = self.partner_id.formal_salutation
        self.informal_salutation = self.partner_id.informal_salutation

    def fillsalutation(self, partner):
        partner.firstname = self.firstname
        partner.lastname = self.lastname
        partner.formal_salutation = self.formal_salutation
        partner.informal_salutation = self.informal_salutation
        partner.formal_partner_salutation = self.formal_salutation_result
        partner.informal_partner_salutation = self.informal_salutation_result
        partner.title = self.title

    def write(self, vals):
        if vals.get('firstname') and vals.get('informal_salutation'):
            informal_salutation = dict(self._fields['informal_salutation'].selection).get(vals.get('informal_salutation'))
            vals.update({'informal_salutation_result': _(informal_salutation)+ ' ' + vals.get('firstname')})
        if vals.get('lastname') and vals.get('formal_salutation'):
            if vals.get('title'):
                title_id = self.env['res.partner.title'].browse(vals.get('title'))
                title = title_id.name or ''
            else:
                title = self.title.name or ''
            formal_salutation = dict(self._fields['formal_salutation'].selection).get(vals.get('formal_salutation'))
            vals.update({'formal_salutation_result': _(formal_salutation)+ ' ' +_(title)+' '+vals.get('lastname')})
        if vals.get('type') == 'opportunity':
            if self.partner_id:
                self.fillsalutation(self.partner_id)
            if vals.get('partner_id'):
                self.fillsalutation(self.env['res.partner'].browse(vals.get('partner_id')))
        return super(CrmSalutation, self).write(vals)

    @api.model
    def create(self, vals):
        res = super(CrmSalutation, self).create(vals)
        if res.contact_name and not (res.firstname and res.lastname):
            name = res.contact_name.split(' ',1)
            if len(name)>=2:
                res.firstname = name[0]
                res.lastname = name[1]
            if len(name) == 1:
                res.firstname = name[0]
        return res

    @api.onchange('contact_name')
    def _onchange_contact_name(self):
        if self.contact_name:
            name = self.contact_name.split(' ',1)
            if len(name)>=2:
                self.firstname = name[0]
                self.lastname = name[1]
            if len(name) == 1:
                self.firstname = name[0]

class SaleOrderSalutation(models.Model):
    _inherit = 'sale.order'

    sale_order_partner_result = fields.Char(string='Partner Salutation')
    salutation_type = fields.Selection([('formal', 'Formal'),
        ('informal', 'Informal')], default='formal', string='Salutation Type')

    @api.onchange('partner_id', 'salutation_type')
    def _onchange_saleorder_salutation(self):
        if self.salutation_type == 'formal':
            self.sale_order_partner_result = self.partner_id.formal_partner_salutation
        elif self.salutation_type == 'informal':
            self.sale_order_partner_result = self.partner_id.informal_partner_salutation
        else:
            self.sale_order_partner_result = False