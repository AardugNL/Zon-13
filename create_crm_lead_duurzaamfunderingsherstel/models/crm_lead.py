# -*- encoding: utf-8 -*-
##############################################################################
##############################################################################

from bs4 import BeautifulSoup

from odoo import api, models


class crm_lead(models.Model):
    _inherit = "crm.lead"

    @api.model
    def totalwall_parser(self, emailBody):
        """This Method returns plain text dict for 
        Template duurzaamfunderingsherstel
        """
        newSoup = BeautifulSoup(emailBody.replace('<br>', '\n').replace('\n\r\n', '\n'), features="lxml")

        # Maintain this list for keys.
        planKeyExtract = {
            'Naam:': ['naam:', 'Naam:', ':Naam:'],
            'Dhr. Voornaam:': ['Dhr. Voornaam:',':Dhr. Voornaam:'],
            'Mevr. Voornaam:': ['Mevr. Voornaam:',':Mevr. Voornaam:'],
            'E-mail:': ['email:', 'E-mailadres:'],
            'Telefoon:': ['telefoon:', 'Telefoonnummer:'],
            'Woonplaats:': ['woonplaats:', 'Woonplaats:', 'woonplaats:'],
            'Postcode:': ['postcode:', 'Postcode:'],
            'plan-street': ['straat:', 'Straat:'],
            'plan-house': ['huisnummer:', 'Huisnummer:']
        }

        def checkForKeyVal(line):
            key = None
            value = None
            for newKey, applicableCaption in planKeyExtract.items():
                for caption in applicableCaption:
                    idx = len(caption) if line.find(caption) == 0 else None
                    if idx and line[idx:]:
                        key = newKey
                        value = line[idx:]
                        break
                else:
                    continue
                break
            return key, value

        newdict = {}
        getlines = []
        for lines in [newSoup.get_text()]:
            getlines = lines.split('\n')
            if getlines[0] and ':Naam:' in getlines[0]:
                getlines[0] = ''.join(getlines[0].partition(':Naam:')[1:])
            if getlines[0] and ':Dhr. Voornaam:' in getlines[0]:
                getlines[0] = ''.join(getlines[0].partition(':Dhr. Voornaam:')[1:])
            if getlines[0] and ':Mevr. Voornaam:' in getlines[0]:
                getlines[0] = ''.join(getlines[0].partition(':Mevr. Voornaam:')[1:])
            if len(getlines) > 1:
                for line in getlines:
                    key, value = checkForKeyVal(line)
                    if key and value:
                        newdict[key] = value

                # Adjust Plan Keys
                newdict['Adres:'] = ' '.join(
                    [x for x in [
                        newdict.get('plan-street', None),
                        newdict.get('plan-house', None)
                    ] if x]
                )

        return newdict

    @api.model
    def totalwall_condition(self, mailMessage, emailBody):
        """Condition for duurzaamfunderingsherstel template."""
        return (mailMessage.company in ['totalwall', 'Totalwall', 'duurzaamfunderingsherstel'] or
                'totalwall' in emailBody)

    @api.model
    def registerCompanyParser(self):
        """Register duurzaamfunderingsherstel Parser Mappin in main."""
        parsers = super(crm_lead, self).registerCompanyParser()
        parsers.append(
            (3,
             self.totalwall_condition,
             self.totalwall_parser)
        )
        return parsers
