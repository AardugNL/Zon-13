# -*- encoding: utf-8 -*-
##############################################################################
##############################################################################

from bs4 import BeautifulSoup
import itertools
import logging
import re

from odoo import api, models, _
from odoo import tools

_logger = logging.getLogger(__name__)


def find_between_r(s, first, last):
    try:
        start = s.rindex(first) + len(first)
        return s[start:s.rindex(last, start)]
    except ValueError:
        return ""


class crm_lead(models.Model):
    _inherit = "crm.lead"

    @api.model
    def isolatieVergelijker_parser(self, emailBody):
        """This Method returns plain text dict for
        Template isolatievergelijker
        """
        plain_text_body = tools.html2plaintext(emailBody)
        newdict = {}
        a = find_between_r(plain_text_body, 'Contactgegevens', 'Beste').split('\n')
        if len(a) > 1:
            naamindex = [i for i, s in enumerate(a) if 'Naam' in s]
            if naamindex and naamindex[0]:
                naam = a[naamindex[0]+1].replace('*', '')
                if naam == ':':
                    newdict['Naam:'] = a[naamindex[0]+2].replace('*', '')
                else:
                    newdict['Naam:'] = naam
            telefoonindex = [i for i, s in enumerate(a) if 'Telefoon' in s]
            if telefoonindex and telefoonindex[0]:
                telefoon = a[telefoonindex[0]+1].replace('*', '')
                if telefoon == ':':
                    newdict['Telefoon:'] = a[telefoonindex[0]+2].replace('*', '')
                else:
                    newdict['Telefoon:'] = telefoon
            emailindex = [i for i, s in enumerate(a) if 'E-mail' in s]
            if emailindex and emailindex[0]:
                email = a[emailindex[0]+1].replace('*', '')
                if email == ':':
                    newdict['E-mail:'] = a[emailindex[0]+3].replace('*', '')
                else:
                    newdict['E-mail:'] = email
            straatnaamindex = [i for i, s in enumerate(a) if 'Straatnaam' in s]
            if straatnaamindex and straatnaamindex[0]:
                straatnaam = a[straatnaamindex[0]+1].replace('*', '')
                if straatnaam == ':':
                    newdict['Straatnaam:'] = a[straatnaamindex[0]+2].replace('*', '')
                else:
                    newdict['Straatnaam:'] = straatnaam
            postcodeindex = [i for i, s in enumerate(a) if 'Postcode' in s]
            if postcodeindex and postcodeindex[0]:
                postcode = a[postcodeindex[0]+1].replace('*', '')
                if postcode == ':':
                    newdict['Postcode:'] = a[postcodeindex[0]+2].replace('*', '')
                else:
                    newdict['Postcode:'] = postcode
            plaatsindex = [i for i, s in enumerate(a) if 'Plaats' in s]
            if plaatsindex and plaatsindex[0]:
                plaats = a[plaatsindex[0]+1].replace('*', '')
                if plaats == ':':
                    newdict['Plaats:'] = a[plaatsindex[0]+2].replace('*', '')
                else:
                    newdict['Plaats:'] = plaats
        return newdict

    @api.model
    def isolatieVergelijker_condition(self, mailMessage, emailBody):
        """Condition for isolatieVergelijker template."""
        return (mailMessage.company == 'isolatievergelijker' or
                'isolatievergelijker' in emailBody)

    @api.model
    def registerCompanyParser(self):
        """Register isolatievergelijker Parser Mappin in main."""
        parsers = super(crm_lead, self).registerCompanyParser()
        parsers.append(
            (2,
             self.isolatieVergelijker_condition,
             self.isolatieVergelijker_parser))
        return parsers
