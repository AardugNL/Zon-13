# -*- encoding: utf-8 -*-

from bs4 import BeautifulSoup
import itertools
import logging
import re

from odoo import api, models, _
from odoo import tools


_logger = logging.getLogger(__name__)
email_body = '''
<p>
Hello %s,
</p>
<p>
A lead has been generated with reference number %s.
</p>
<p>
Thanks.
</p>
'''

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
    def create(self, vals):
        result = super(crm_lead, self).create(vals)
        if vals.get('email_from'):
            if '<' and '>' in vals.get('email_from'):
                pemail = vals.get('email_from').split('<')
                result.email_from = pemail[1].replace(
                    "u'", " ").replace(">'", "").replace('>', '')
            else:
                result.email_from = vals.get('email_from')
        return result

    @api.model
    def registerCompanyParser(self):
        """Return company mapping(list of tuple) for extension of new templates
        for lead information parsing from incoming email body.

        i.e: (priority, condition, parser) where #1 is condition for company
        and #2 is for collecting information from email body parser.

        priority: This parser executed in order by priority.

        condition: This can be a function which can accept two arguments as
        following.
        mailMessage = respected mail.message redord.
        emailBody = html email body which received and parsing in progress for
        crm lead record.

        parser: This must be your parser and should return dictionary with
        repected valid values to be filled on lead record. Check code of
        create_crm_lead module for more detail. If key(condition) returns
        True value(parser) will be called with email body in argument.

        You can override this function and add your template setup.
        """
        return []

    @api.model
    def _build_valid_dict(self, newdict):
        valid_dict = {}

        contactNames = []
        if newdict.get('Voornaam:', '') or newdict.get('Voornaam', ''):
            contactNames.append(
                clear_string(newdict.get('Voornaam:', '') or
                             newdict.get('Voornaam', ''),
                             True))
        if newdict.get('Naam:', '') or newdict.get('Naam', ''):
            contactNames.append(
                clear_string(newdict.get('Naam:', '') or
                             newdict.get('Naam', ''),
                             True))
        if newdict.get('Achternaam:', '') or newdict.get('Achternaam', ''):
            contactNames.append(
                clear_string(newdict.get('Achternaam:', '') or
                             newdict.get('Achternaam', ''),
                             True))
        if newdict.get('Contact:', ''):
            contactNames.append(
                clear_string(newdict.get('Contact:', ''), True))
        if contactNames:
            valid_dict['contact_name'] = ' '.join(contactNames)
        if newdict.get('E-mail:', ''):
            email = clear_string(newdict.get('E-mail:', ''), True)
            splitted_email = email.split()
            if len(splitted_email) > 1:
                email = splitted_email[0]
            valid_dict['email_from'] = email
        if newdict.get('E-mailadres:', ''):
            email = clear_string(newdict.get('E-mailadres:', ''), True)
            splitted_email = email.split()
            if len(splitted_email) > 1:
                email = splitted_email[0]
            valid_dict['email_from'] = email
        if newdict.get('E-mail adres:', ''):
            email = clear_string(newdict.get('E-mail adres:', ''), True)
            splitted_email = email.split()
            if len(splitted_email) > 1:
                email = splitted_email[0]
            valid_dict['email_from'] = email
        if newdict.get('Email adres:', ''):
            email = clear_string(newdict.get('Email adres:', ''), True)
            splitted_email = email.split()
            if len(splitted_email) > 1:
                email = splitted_email[0]
            valid_dict['email_from'] = email
        if (newdict.get('Telefoon:', '') or
                newdict.get('Telefoonnummer:', '') or
                newdict.get('Telefoonnummer 1', '') or
                newdict.get('Tel.:', '')):
            valid_dict['phone'] = clear_string(
                newdict.get('Telefoon:', '') or
                newdict.get('Telefoonnummer:', '') or
                newdict.get('Telefoonnummer 1', '') or
                newdict.get('Tel.:', ''),
                True)
        if newdict.get('Mobiel:', ''):
            valid_dict['mobile'] = clear_string(
                newdict.get('Mobiel:', ''), True)

        if newdict.get('Adres:', '') or newdict.get('Straat:', ''):
            valid_dict['street'] = clear_string(
                newdict.get('Adres:', '') or newdict.get('Straat:', ''), True)
        if newdict.get('Straatnaam:', ''):
            if 'google' in newdict.get('Straatnaam:', '').lower():
                street = newdict.get('Straatnaam:', '')
                street = re.sub(r'\([^)]*\)', '', street)
            else:
                street = newdict.get('Straatnaam:', '')
            valid_dict['street'] = clear_string(street, True)

        if newdict.get('Postcode:', ''):
            valid_dict['zip'] = clear_string(
                newdict.get('Postcode:', ''), True)
        if newdict.get('Postal:', ''):
            valid_dict['zip'] = clear_string(newdict.get('Postal:', ''), True)
        if (newdict.get('Woonplaats:', '') or
                newdict.get('Plaats:', '') or
                newdict.get('Stad:', '') or
                newdict.get('Plaatsnaam:', '')):
            valid_dict['city'] = clear_string(
                newdict.get('Woonplaats:', '') or
                newdict.get('Plaats:', '') or
                newdict.get('Stad:', '') or
                newdict.get('Plaatsnaam:', ''),
                True)
        if newdict.get('Toelichting:', ''):
            valid_dict['description'] = clear_string(
                newdict.get('Toelichting:', ''), True)
        return valid_dict

    @api.model
    def create_lead_from_email_body(self):
        mm_obj = self.env['mail.message']
        m_mail_obj = self.env['mail.mail']
        lead_obj = self.env['crm.lead']
        ir_model_data = self.env['ir.model.data']
        mail_comp_obj = self.env['mail.compose.message']
        mailLeadSrc = self.env['lead.email.lead.source']
        mailLeadCateg = self.env['lead.email.lead.category']
        # customer = self.env['res.partner']
        lead_id = self.browse(self.env.context.get('active_id'))
        if lead_id.email_from:
            companyname = ''
            emailfromat = lead_id.email_from.split('@')
            if len(emailfromat) == 2:
                emailfromdot = emailfromat[1].split('.')
                companyname = emailfromdot[0]
            subtype_id = self.env.ref('crm.mt_lead_create')
            message_ids = mm_obj.search([('res_id', '=', lead_id.id),
                                         ('model', '=', 'crm.lead'),
                                         ('message_type', '=', 'email'),
                                         ('subtype_id', '=', subtype_id.id)])
            for messageid in message_ids:
                messageid.company = companyname
    
            _logger.info(
                '%s create crm lead from mail %s', len(message_ids), lead_id.id)
            _logger.info('Crm Lead Record ID ::::: (%s)', lead_id.id)
            _logger.info('Crm Lead Subject Name ::::: %s', lead_id.name or '')
            if len(message_ids) < 1:
                return True
            html_body = message_ids.read(['body'])[0].get('body')
            newdict = {}
            try:
                conditionalParsers = sorted(self.registerCompanyParser(),
                                            key=lambda x: x[0])
                for priority, condition, parser in conditionalParsers:
                    if condition(mailMessage=messageid, emailBody=html_body):
                        newdict.update(parser(emailBody=html_body))
                # Write valid values to lead record.
                if newdict:
                    valid_dict = self._build_valid_dict(newdict)
                    if valid_dict:
                        lead_id.write(valid_dict)
                        lead_id.email_description = html_body
                        mailLeadSrcId = mailLeadSrc.search(
                            [('domain', '=', companyname)])
                        _logger.info('CRM LEAD EMAIL COMPANY: %s', mailLeadSrcId)
                        if mailLeadSrcId:
                            PossibleCategoryIds = mailLeadCateg.search(
                                [('lead_email_lead_source', '=', mailLeadSrcId.id)],
                                order="priority")
                            if PossibleCategoryIds:
                                plain_text_body = tools.html2plaintext(html_body)
                                for categ in PossibleCategoryIds:
                                    if (categ.content and (categ.content in html_body or
                                                           categ.content in plain_text_body)):
                                        _logger.info('CRM LEAD EMAIL CATEGORY: %s', categ.lead_category)
                                        lead_id.lead_category = categ.lead_category and categ.lead_category.id or False
                                        lead_id.lead_lead_source = mailLeadSrcId.lead_source and mailLeadSrcId.lead_source.id or False
                                        lead_id.tag_ids = categ.lead_category.tag_ids
                                    if not categ.content:
                                        _logger.info('CRM LEAD EMAIL CATEGORY 2: %s', categ.lead_category)
                                        lead_id.lead_category = categ.lead_category and categ.lead_category.id or False
                                        lead_id.lead_lead_source = mailLeadSrcId.lead_source and mailLeadSrcId.lead_source.id or False
                                        lead_id.tag_ids = categ.lead_category.tag_ids
                                    # TODO : below code usage are convert Lead to opprtunity, stage set
                                    # if categ.lead_category.stage_id:
                                    #     partner_id = customer.create({
                                    #                                 'name': lead_id.contact_name or '',
                                    #                                 'street':lead_id.street or '',
                                    #                                 'street2':lead_id.street2 or '',
                                    #                                 'city':lead_id.city or '',
                                    #                                 'zip':lead_id.zip or '',
                                    #                                 'email':lead_id.email_from or '',
                                    #                                 'phone':lead_id.phone or ''})
                                    #     if partner_id:
                                    #         lead_id.convert_opportunity(partner_id.id, user_ids=self.env.user.ids, team_id=lead_id.team_id.id)
                                    #         lead_id.stage_id = categ.lead_category.stage_id and categ.lead_category.stage_id.id or False
    
                        netherlands = self.env['res.country'].search(
                            [('name', '=', 'Netherlands')])
                        binnenland = self.env['account.fiscal.position'].search(
                            [('name', '=', 'Binnenland')])
                        days15 = self.env['account.payment.term'].search(
                            [('name', '=', '15 Days')])
                        partner = lead_id.partner_id if lead_id.partner_id else False
                        if partner:
                            partner.country_id = netherlands and netherlands.id or False
                            partner.property_account_position_id = binnenland and binnenland.id or False
                            partner.lang = 'nl_NL'
                            partner.property_payment_term_id = days15 and days15.id or False
                        elif not partner:
                            lead_id.country_id = netherlands and netherlands.id or False
                        
                        email_to = valid_dict.get('email_from')
                        if not email_to:
                            email_to = self.email_from or ''
                        if email_to:
                            email_template = ir_model_data.get_object_reference(
                                'create_crm_lead',
                                'email_template_lead_create_welcome_new_mail')[1]
                            template = mail_comp_obj.generate_email_for_composer(
                                email_template, lead_id.id)
                            vals = {
                                'auto_delete': True, 
                                'email_to': email_to,
                                'subject': template['subject'],
                                'body_html': template['body']
                            }
                            mail_id = m_mail_obj.create(vals)
                            lead_id.message_post(
                                body=_('sent mail is %s.') % (mail_id.body_html)) 
                            mail_id.send()
                            self.email_description = html_body
                    else:
                        mailLeadSrcId = mailLeadSrc.search(
                            [('domain', '=', companyname)])
                        _logger.info('CRM LEAD EMAIL COMPANY: %s', mailLeadSrcId)
                        if mailLeadSrcId:
                            PossibleCategoryIds = mailLeadCateg.search(
                                [('lead_email_lead_source', '=', mailLeadSrcId.id)],
                                order="priority")
                            if PossibleCategoryIds:
                                plain_text_body = tools.html2plaintext(html_body)
                                for categ in PossibleCategoryIds:
                                    if (categ.content and (categ.content in html_body or
                                                           categ.content in plain_text_body)):
                                        _logger.info('CRM LEAD EMAIL CATEGORY: %s', categ.lead_category)
                                        lead_id.lead_category = categ.lead_category and categ.lead_category.id or False
                                        lead_id.lead_lead_source = mailLeadSrcId.lead_source and mailLeadSrcId.lead_source.id or False
                                        lead_id.tag_ids = categ.lead_category.tag_ids
                                    if not categ.content:
                                        _logger.info('CRM LEAD EMAIL CATEGORY 2: %s', categ.lead_category)
                                        lead_id.lead_category = categ.lead_category and categ.lead_category.id or False
                                        lead_id.lead_lead_source = mailLeadSrcId.lead_source and mailLeadSrcId.lead_source.id or False
                                        lead_id.tag_ids = categ.lead_category.tag_ids
                                    # TODO : below code usage are convert Lead to opprtunity, stage set
                                    # if categ.lead_category.stage_id:
                                    #     partner_id = customer.create({
                                    #                                 'name': lead_id.contact_name or '',
                                    #                                 'street':lead_id.street or '',
                                    #                                 'street2':lead_id.street2 or '',
                                    #                                 'city':lead_id.city or '',
                                    #                                 'zip':lead_id.zip or '',
                                    #                                 'email':lead_id.email_from or '',
                                    #                                 'phone':lead_id.phone or ''})
                                    #     if partner_id:
                                    #         lead_id.convert_opportunity(partner_id.id, user_ids=self.env.user.ids, team_id=lead_id.team_id.id)
                                    #         lead_id.stage_id = categ.lead_category.stage_id and categ.lead_category.stage_id.id or False

            except:
                # Silently pass,
                # Email format is not known hence it will perform lead creation in
                # Odoo's default way, that is, using the header information.
                pass

        return True
