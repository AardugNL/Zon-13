# -*- encoding: utf-8 -*-

# DEMO for new template.

from odoo import api, models
from odoo import tools


def clear_string(strng, strip=False):
    if strip:
        return strng.strip()
    return strng.replace('\n', '').replace('\r', '').strip()


def find_between_r(s, first, last):
    try:
        start = s.rindex(first) + len(first)
        return s[start:s.rindex(last, start)]
    except ValueError:
        return ""


class crm_lead(models.Model):
    _inherit = "crm.lead"

    @api.model
    def offertevergelijker_parser(self, emailBody):
        """This Method returns plain text dict for
        Template offertevergelijker.
        """
        plain_text_body = tools.html2plaintext(emailBody)
        newdict = {}
        a = find_between_r(plain_text_body,
                           'Spouwmuurisolatie offerte details',
                           'Zijn er nog vragen? ').split('\n')
        if len(a) > 1:
            emailindex = [i for i, s in enumerate(a) if 'Email:' in s]
            if emailindex and emailindex[0]:
                finalemailindex = emailindex[0] + 1
                newdict['E-mail:'] = a[finalemailindex]
            telephoneindex = [i for i, s in enumerate(a) if 'Telefoon:' in s]
            if telephoneindex and telephoneindex[0]:
                finaltelephone = telephoneindex[0] + 1
                newdict['Telefoon:'] = a[finaltelephone]
            if a[10]:
                naam = a[10].replace(' ', ' ')
                newdict['Naam:'] = naam
            if a[11]:
                newdict['Straatnaam:'] = a[11]
            if a[12]:
                code = a[12]
                addressstring = code.split(' ')
                if len(addressstring) > 2:
                    newdict['Postcode:'] = addressstring[0]
                    newdict['Plaats:'] = addressstring[-1]
        return newdict

    @api.model
    def offertevergelijker_condition(self, mailMessage, emailBody):
        return (mailMessage.company == 'offertevergelijker' or
                'offertevergelijker' in emailBody)

    # Important handler code.
    @api.model
    def registerCompanyParser(self):
        parsers = super(crm_lead, self).registerCompanyParser()
        parsers.append(
            (8,
             self.offertevergelijker_condition,
             self.offertevergelijker_parser),
        )
        return parsers
