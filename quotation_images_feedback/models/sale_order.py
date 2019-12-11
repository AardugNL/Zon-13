# -*- coding: utf-8 -*-

from odoo import api, fields, models, _, tools
from datetime import datetime
import re

DTFORMAT = tools.DEFAULT_SERVER_DATETIME_FORMAT

class SaleOrderLine(models.Model):
    """ Question Formulier id add """

    _inherit = "sale.order.line"

    question_frm_id = fields.Many2one(related='order_id.question_frm_id', string='Project Formulier')

class SaleOrder(models.Model):
    """ Question Formulier Tab """

    _inherit = "sale.order"

    soort = fields.Selection(string='Soort', selection=[('aanbouw', 'aanbouw'),
        ('hoek', 'hoek'), ('gevel', 'kopgevel'), ('groot deel', 'groot deel')],
        default='aanbouw')

    def _get_default_formulier(self):
        opportunity_id = self.env.context.get('default_opportunity_id') or False
        if opportunity_id:
            CrmLead = self.env['crm.lead'].browse(opportunity_id)
            return CrmLead.question_frm_id.id

    question_frm_id = fields.Many2one('question.formulier', default=_get_default_formulier, string='Project Formulier')

    @api.model
    def create(self,vals):
        res = super(SaleOrder, self).create(vals)
        if res.sale_order_template_id:
            res.fill_drawing_images()
        oppo = res.opportunity_id
        if oppo:
            res.user_id = oppo.user_id.id or self.env.user.id
            if oppo.question_frm_id:
                res.question_frm_id = oppo.question_frm_id.id
                res.question_frm_id.date_report = res.create_date.date()
                res.question_frm_id.state = 'task'
            if oppo.soort:
                res.soort = oppo.soort
        return res

    def write(self,vals):
        res = super(SaleOrder, self).write(vals)
        if vals.get('sale_order_template_id'):
            self.fill_drawing_images()
        if vals.get('opportunity_id'):
            oppo = self.opportunity_id
            if oppo:
                self.user_id = oppo.user_id.id or self.env.user.id
                if oppo.question_frm_id:
                    self.question_frm_id = oppo.question_frm_id.id
                    self.question_frm_id.state = 'task'
                if oppo.soort:
                    self.soort = oppo.soort
        return res

    @api.model
    def fill_drawing_images(self):
        footer = ""
        description = ""
        imgDict = {}
        f_variables = ""
        if self.website_description:
            description = self.website_description.encode('utf-8')
        if self.website_desc_footer:
            footer = self.website_desc_footer.encode('utf-8')

        if description:# or footer:
            # custom object replacement for sale order fields value 
            c_variables = re.findall(
                    b'\${custom:.*?}', description)
            if footer:
                c_variables.extend(re.findall(
                        b'\${custom:.*?}', footer))
            if c_variables:
                for custom in list(set(c_variables)):
                    custom_object = custom.decode('utf-8')
                    field = custom_object.split('}')[0][16:]
                    if field in self._fields:
                        value = self.read([field])
                        if value[0].get(field):
                            if field == 'amount_total':
                                imgDict.update(
                                    {custom_object: str("{:.2f}".format(value[0].get(field)))})
                            elif type(value[0].get(field)) is tuple:
                                imgDict.update(
                                    {custom_object: str(value[0].get(field)[1])})
                            else:
                                imgDict.update(
                                    {custom_object: str(value[0].get(field))})
                        else:
                            imgDict.update({custom_object: ''})

            if self.question_frm_id:
                # dynamic value for custom and project formulier object
                f_variables = re.findall(
                    b'\${formulier:.*?}', description)
                if footer:
                    f_variables.extend(re.findall(
                        b'\${formulier:.*?}', footer))
                if f_variables:
                    for custom in  list(set(f_variables)):
                        custom_object = custom.decode('utf-8')
                        field = custom_object.split('}')[0][19:]
                        if field in self.question_frm_id._fields:
                            value = self.question_frm_id.read([field])
                            if value[0].get(field):
                                if type(value[0].get(field)) is tuple:
                                    imgDict.update(
                                        {custom_object: str(value[0].get(field)[1])})
                                else:
                                    imgDict.update(
                                        {custom_object: str(value[0].get(field))})
                            else:
                                 imgDict.update({custom_object: ''})
            if self.opportunity_id:
                # dynamic value for opportunity
                o_variables = re.findall(
                    b'\${opportunity:.*?}', description)
                if footer:
                    o_variables.extend(re.findall(
                        b'\${opportunity:.*?}', footer))
                if o_variables:
                    for oppo in list(set(o_variables)):
                        oppo_object = oppo.decode('utf-8')
                        field = oppo_object.split('}')[0][21:]
                        if field == 'salutation':
                            salutation = 'Geachte '
                            if self.opportunity_id.title:
                                salutation = salutation + self.opportunity_id.title.name
                            else:
                                salutation = salutation + 'heer/mevrouw'
                            imgDict.update(
                                        {oppo_object: salutation})
                        if field in self.opportunity_id._fields:
                            value = self.opportunity_id.read([field])
                            if value[0].get(field):
                                if type(value[0].get(field)) is tuple:
                                    imgDict.update(
                                        {oppo_object: str(value[0].get(field)[1])})
                                else:
                                    imgDict.update(
                                        {oppo_object: str(value[0].get(field))})
                            else:
                                imgDict.update({oppo_object: ''})

            # dynamic value of 3 field in quote template
            dutch_date = {'January': 'januari', 'February': 'februari', 'March': 'maart', 'May': 'mei', 'June': 'juni', 'July': 'juli', 'August': 'augustus', 'October': 'oktober', 'Monday': 'maandag', 'Tuesday': 'dinsdag', 'Wednesday': 'woensdag', 'Thursday': 'donderdag', 'Friday': 'vrijdag', 'Saturday': 'zaterdag', 'Sunday': 'zondag'}
            if f_variables:
                if self.question_frm_id.lead_id and self.question_frm_id.lead_id.soort:
                    imgDict.update({'${formulier:object.soort}': str(
                        self.question_frm_id.lead_id.soort)})
                else:
                    imgDict.update({'${formulier:object.soort}': ''})
                if self.question_frm_id.lead_id and self.question_frm_id.lead_id.user_id:
                    imgDict.update({'${formulier:object.salesman}': str(
                        self.question_frm_id.lead_id.user_id.name)})
                else:
                    imgDict.update({'${formulier:object.salesman}': ''})
                if self.question_frm_id.date_opportunity:
                    date_string = self.question_frm_id.date_opportunity.strftime('%A %d %B')
                    if self._context.get('lang') == 'nl_NL':
                        for i, j in dutch_date.items():
                            date_string = date_string.replace(i,j)
                    imgDict.update({'${formulier:object.date_opportunity}': date_string})
                else:
                    imgDict.update({'${formulier:object.date_opportunity}': ''})

            for key, val in imgDict.items():
                description = description.replace(
                    key.encode('utf-8'), val.encode('utf-8'))
            if footer:
                for key, val in imgDict.items():
                    footer = footer.replace(
                        key.encode('utf-8'), val.encode('utf-8'))
                self.website_desc_footer = footer
            self.website_description = description
        return self.website_description

class OrderTemplate(models.Model):
    """ Sale Order Template """

    _inherit = "sale.order.template"

    template_video_ids = fields.One2many('order.video', 'order_template_id', track_visibility='always', string='Video')

class OrderTemplateVideo(models.Model):
    """ new model for add videos in sale order template"""

    _inherit = 'order.video'

    order_template_id = fields.Many2one('sale.order.template', 'Related Template', copy=True, readonly=True)
