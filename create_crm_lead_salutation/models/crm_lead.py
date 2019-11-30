# -*- encoding: utf-8 -*-

import logging

from odoo import api, models, _

_logger = logging.getLogger(__name__)

def clear_string(strng, strip=False):
    if strip:
        return strng.strip()
    return strng.replace('\n', '').replace('\r', '').strip()

class crm_lead(models.Model):
    _inherit = "crm.lead"

    @api.model
    def _build_valid_dict(self, newdict):
        valid_dict = super(crm_lead, self)._build_valid_dict(newdict)
        contactNames = []
        name_dict = newdict.get('Naam:', '') or newdict.get('Naam', '')
        if newdict.get('Voornaam:', '') or newdict.get('Voornaam', ''):
            contactNames.append(
                clear_string(newdict.get('Voornaam:', '') or
                             newdict.get('Voornaam', ''),
                             True))
        if name_dict:
            contactNames.append(
                clear_string(name_dict,True))
            if len(name_dict.split(' ')) > 1:
                valid_dict['firstname'] = name_dict.split(' ')[0].strip()
                valid_dict['lastname'] = name_dict.split(' ')[1].strip()
                if len(name_dict.split(' ')) > 2:
                    valid_dict['lastname'] = name_dict.split(' ')[1].strip() +' '+ name_dict.split(' ')[2].strip()
            else:
                valid_dict['firstname'] = name_dict
        if newdict.get('Achternaam:', '') or newdict.get('Achternaam', ''):
            contactNames.append(
                clear_string(newdict.get('Achternaam:', '') or
                             newdict.get('Achternaam', ''),
                             True))
        if newdict.get('Dhr. Voornaam:', '') or newdict.get('Dhr. Voornaam', ''):
            name = clear_string(newdict.get('Dhr. Voornaam:', ''),True)
            first_name = name.split('Achternaam:')[0].strip()
            last_name = name.split('Achternaam:')[1].strip()
            if first_name and last_name:
                contactNames.append(first_name+' '+last_name)
            valid_dict['firstname'] = first_name
            valid_dict['lastname'] = last_name
            title = self.env['res.partner.title'].search([('name', 'like', 'Mister')], limit=1)
            if title:
                valid_dict['title'] = title.id
        elif name_dict and 'De heer' in name_dict:
            name = clear_string(name_dict,True)
            only_name = name.split('De heer ')[1]
            if len(only_name.split(' ')) > 1:
                valid_dict['firstname'] = only_name.split(' ')[0].strip()
                valid_dict['lastname'] = only_name.split(' ')[1].strip()
                contactNames = [only_name]
                if len(only_name.split(' ')) > 2:
                    valid_dict['lastname'] = only_name.split(' ')[1].strip() +' '+ only_name.split(' ')[2].strip()
            else:
                valid_dict['firstname'] = only_name
                contactNames = [only_name]
            title = self.env['res.partner.title'].search([('name', 'like', 'Mister')], limit=1)
            if title:
                valid_dict['title'] = title.id
        valid_dict['formal_salutation'] = 'dear'
        valid_dict['informal_salutation'] = 'best'
        if newdict.get('Mevr. Voornaam:', '') or newdict.get('Mevr. Voornaam', ''):
            name = clear_string(newdict.get('Mevr. Voornaam:', ''),True)
            first_name = name.split('Achternaam:')[0].strip()
            last_name = name.split('Achternaam:')[1].strip()
            if first_name and last_name:
                contactNames.append(first_name+' '+last_name)
            valid_dict['firstname'] = first_name
            valid_dict['lastname'] = last_name
            title = self.env['res.partner.title'].search([('name', 'like', 'Madam')], limit=1)
            if title:
                valid_dict['title'] = title.id
        elif name_dict and 'Mevrouw' in name_dict:
            name = clear_string(name_dict,True)
            only_name = name.split('Mevrouw ')[1]
            if len(only_name.split(' ')) > 1:
                valid_dict['firstname'] = only_name.split(' ')[0].strip()
                valid_dict['lastname'] = only_name.split(' ')[1].strip()
                contactNames = [only_name]
                if len(only_name.split(' ')) > 2:
                    valid_dict['lastname'] = only_name.split(' ')[1].strip() +' '+ only_name.split(' ')[1].strip()
            else:
                valid_dict['firstname'] = only_name
                contactNames = [only_name]
            title = self.env['res.partner.title'].search([('name', 'like', 'Mister')], limit=1)
            if title:
                valid_dict['title'] = title.id
        if contactNames:
            valid_dict['contact_name'] = ' '.join(contactNames)
        return valid_dict

