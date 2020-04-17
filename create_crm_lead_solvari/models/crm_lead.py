# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################


import logging


from odoo import api, models, _
from odoo import tools


_logger = logging.getLogger(__name__)


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
    def solvari_parser(self, emailBody):
        """ This Method returns plain text dict for 
        Template solvari
        """
        plain_text_body = tools.html2plaintext(emailBody)
        newdict = {}

        a = find_between_r(
            plain_text_body, 'Campagne', 'Alle informatie').split('\n')

        if len(a) > 1:
            naamindex = [i for i, s in enumerate(a) if 'Naam' in s]
            if naamindex and naamindex[0]:
                plain_naam = a[naamindex[0]].replace('*', '')
                naam = plain_naam.split('Naam')
                if len(naam) == 2:
                    # newdict['Campagne:'] = naam[1]
                    if naam[1] == ':':
                        newdict['Naam:'] = a[naamindex[0 ] +5]
                    else:
                        newdict['Naam:'] = naam[1]
            adresindex = [i for i, s in enumerate(a) if 'Adres' in s]
            if adresindex and adresindex[0]:
                plain_adres = a[adresindex[0]].replace('*', '')
                adres = plain_adres.split('Adres')
                if len(adres) == 2 and adres[1]:
                    if adres[1] == ':':
                        full_adres = a[adresindex[0] + 5].split(',')
                        zip_city = full_adres[1].replace(' ', '')
                        newdict['Adres:'] = full_adres[0]
                        newdict['Postcode:'] = zip_city[:6]
                        newdict['Plaatsnaam:'] = zip_city[6:]
                    else:
                        newdict['Adres:'] = adres[1]
                if adresindex[0] + 1 and newdict.get('Naam:', None):
                    adres_second = a[adresindex[0] + 5].split(' ')
                    if len(adres_second) == 2:
                        newdict['Postcode:'] = adres_second[0]
                        newdict['Plaatsnaam:'] = adres_second[1]
            emailindex = [i for i, s in enumerate(a) if 'E-mail' in s]
            if emailindex and emailindex[0]:
                plain_email = a[emailindex[0]].replace('*', '')
                email = plain_email.split('E-mail')
                if len(email) == 2:
                    if email[1] == 'adres:':
                        newdict['E-mail:'] = a[emailindex[0] + 5]
                    else:
                        newdict['E-mail:'] = email[1]
            telindex = [i for i, s in enumerate(a) if 'Tel.' in s]
            if telindex and telindex[0]:
                newdict['Tel.:'] = a[telindex[0] + 5]
            phoneindex = [i for i, s in enumerate(a)
                          if 'Telefoonnummer 1' in s]
            if phoneindex and phoneindex[0]:
                plain_telephone = a[phoneindex[0]].replace('*', '')
                telephone = plain_telephone.split('Telefoonnummer 1')
                if len(telephone) == 2:
                    if telephone[1]:
                        if telephone[1].strip()[-3] == '[':
                            tele = telephone[1].split(telephone[1].strip()[-3])
                            if len(tele) == 2:
                                newdict['Telefoonnummer 1'] = tele[0]
                        else:
                            newdict['Telefoonnummer 1'] = telephone[1]
            # New Template with blue balls.
            if (not newdict.get('Naam:', None)) and '*Voornaam*' in a:
                newdict['Naam:'] = a[a.index('*Voornaam*') + 5]
            if (not newdict.get('Naam:', None)) and '*Naam*' in a:
                newdict['Naam:'] = a[a.index('*Naam*') + 5]
            if (not newdict.get('Adres:', None)) and '*Adres*' in a:
                lineOne = 1
                if not a[a.index('*Adres*') + lineOne]:
                    lineOne = 2
                newdict['Adres:'] = a[a.index('*Adres*') + lineOne]
                if a[a.index('*Adres*') + lineOne + 1]:
                    zipCity = a[a.index('*Adres*') + lineOne + 1].split(' ')
                    if len(zipCity) >= 2:
                        if not newdict.get('Postcode:', None):
                            newdict['Postcode:'] = zipCity[0]
                        if not newdict.get('Plaatsnaam:', None):
                            newdict['Plaatsnaam:'] = zipCity[1]
            if (not newdict.get('E-mail:', None)) and '*E-mail*' in a:
                newdict['E-mail:'] = a[a.index('*E-mail*') + 5]
            if ((not newdict.get('Telefoonnummer 1', None)) and
                    '*Telefoonnummer 1*' in a):
                newdict['Telefoonnummer 1'] = a[a.index('*Telefoonnummer 1*') + 5]
        elif not len(a) > 1:
            a = find_between_r(
                plain_text_body, 'Onlangs heb', 'terug').split(',')
            newdict['Toelichting:'] = a[0].replace('[1]', '') + 'terug.'
        return newdict

    @api.model
    def solvari_condition(self, mailMessage, emailBody):
        """Condition for solvari template."""
        return (mailMessage.company == 'solvari' or
                'solvari' in emailBody)

    @api.model
    def registerCompanyParser(self):
        """Register Solavari Parser Mappin in main."""
        parsers = super(crm_lead, self).registerCompanyParser()
        parsers.append(
            (2,
             self.solvari_condition,
             self.solvari_parser))
        return parsers
