# -*- encoding: utf-8 -*-
##############################################################################
#                                                                            #
#                                                                            #
##############################################################################

import itertools
import logging

from bs4 import BeautifulSoup

from odoo import api, models
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
    def zonnepanelenvergelijker_parser(self, emailBody):
        """This Method returns plain text dict for
        Template zonnepanelenvergelijker.
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
        else:
            soup = BeautifulSoup(emailBody)
            all_tables_rows = soup.find_all("tr")
            if not len(all_tables_rows) > 0:
                newSoup = BeautifulSoup(
                    emailBody.replace('<br>', '\r\n').replace(
                        '<br/>', '\r\n').replace('</br>', '\r\n'))
                all_text = [newSoup.get_text()]
            else:
                all_text = []
            datasets = []
            if len(all_text) > 0:
                get = []
                b = ''
                getline = []
                for i in all_text:
                    b = i.replace('\r\n', ',')
                get.append(b)
                for line in get:
                    getline = line.split(',')
                for lin in getline:
                    myline = lin.split(':')
                    if len(myline) == 2:
                        key = myline[0] + ':'
                        value = myline[1]
                        newdict[key] = value

            for row in all_tables_rows:
                sub_datasets = []
                for td in row.find_all("td"):
                    tds = td.get_text().replace('\n', '')
                    sub_datasets.append(tds)
                datasets.append(dict(itertools.izip_longest(
                    *[iter(sub_datasets)] * 2, fillvalue="")))
            for dict_val in datasets:
                for dict_key in dict_val.keys():
                    key = ''
                    val = ''
                    if dict_key:
                        val = clear_string(dict_val[dict_key]) if dict_val[dict_key] else ''
                        key = clear_string(dict_key)
                        newdict.update({key: val})
        return newdict

    @api.model
    def zonnepanelenvergelijker_condition(self, mailMessage, emailBody):
        """Condition for zonnepanelenvergelijker template."""
        return (mailMessage.company == 'zonnepanelenvergelijker' or
                'zonnepanelenvergelijker' in emailBody)

    @api.model
    def registerCompanyParser(self):
        """Register Zonnepanelenvergelijker Parser Mappin in main."""
        parsers = super(crm_lead, self).registerCompanyParser()
        parsers.append(
            (1,
             self.zonnepanelenvergelijker_condition,
             self.zonnepanelenvergelijker_parser))
        return parsers
