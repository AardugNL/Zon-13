# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################


from odoo import models, fields, api, tools
import re

class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.depends('street')
    def _split_street(self):
        """Splits street value into sub-fields.
        Recomputes the fields of STREET_FIELDS when `street` of a partner is updated"""
        street_fields = self.get_street_fields()
        for partner in self:
            if not partner.street:
                for field in street_fields:
                    partner[field] = None
                continue

            street_format = '%(street_name)s %(street_number)s/%(street_number2)s'
            street_raw = partner.street
            vals = self._split_street_with_params(street_raw, street_format)
            # assign the values to the fields
            for k, v in vals.items():
                partner[k] = v
            for k in set(street_fields) - set(vals):
                partner[k] = None

    def _set_street(self):
        """Updates the street field.
        Writes the `street` field on the partners when one of the sub-fields in STREET_FIELDS
        has been touched"""
        street_fields = self.get_street_fields()
        for partner in self:
            street_format = '%(street_name)s %(street_number)s/%(street_number2)s'
            previous_field = None
            previous_pos = 0
            street_value = ""
            separator = ""
            # iter on fields in street_format, detected as '%(<field_name>)s'
            for re_match in re.finditer(r'%\(\w+\)s', street_format):
                # [2:-2] is used to remove the extra chars '%(' and ')s'
                field_name = re_match.group()[2:-2]
                field_pos = re_match.start()
                if field_name not in street_fields:
                    raise UserError(_("Unrecognized field %s in street format.") % field_name)
                if not previous_field:
                    # first iteration: add heading chars in street_format
                    if partner[field_name]:
                        street_value += street_format[0:field_pos] + partner[field_name]
                else:
                    # get the substring between 2 fields, to be used as separator
                    separator = street_format[previous_pos:field_pos]
                    if street_value and partner[field_name]:
                        street_value += separator
                    if partner[field_name]:
                        street_value += partner[field_name]
                previous_field = field_name
                previous_pos = re_match.end()

            # add trailing chars in street_format
            street_value += street_format[previous_pos:]
            partner.street = street_value

class Crm_Lead(models.Model):
    _inherit = "crm.lead"

    subject_opportunity = fields.Text(string="Subject On Opportunity")

    def _convert_opportunity_data(self, customer, team_id=False):
        res = super(Crm_Lead,self)._convert_opportunity_data(customer, team_id)
        city = ''
        partner_name = ''
        street_name = ''
        street_number = ''
        lead_category = ''
        oldName = self.name
        if customer:
            if customer.city:
                city = customer.city
            if customer.name:
                partner_name = customer.name 
            if customer.street_name:
                street_name = customer.street_name
            if customer.street_number or customer.street_number2:
                street_number = customer.street_number or customer.street_number2
            if self.lead_category.name:
                lead_category = self.lead_category.name
            merge = ''.join([
                            tools.ustr(city+'-') if city else '',
                            tools.ustr(partner_name+'-') if partner_name else '',
                            tools.ustr(street_name+' ') if street_name else '',
                            tools.ustr(street_number) if street_number else '',
                            tools.ustr('-'+lead_category) if lead_category else ''
                            ])
            res.update({'subject_opportunity': oldName,'name': merge})
        return res