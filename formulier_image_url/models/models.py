# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Caret IT Solutions Pvt. Ltd. (Website: www.caretit.com).           # 
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

import base64
import urllib.request
import requests
from PIL import Image
from io import BytesIO
from odoo.exceptions import Warning
from odoo import api, fields, models, _


class CrmLead(models.Model):
    _inherit = "crm.lead"


    image = fields.Binary(related="question_frm_id.image", string="Overview photo object", track_visibility='always', readonly=False)
    web_url = fields.Char(related="question_frm_id.web_url", string='Image URL', help='Automatically sanitized HTML contents', readonly=False)

    @api.onchange('web_url')
    def onchange_image(self):
        link = self.web_url
        try:
            if link:
                headers = {
                        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) ' 
                        'AppleWebKit/537.11 (KHTML, like Gecko) '
                        'Chrome/23.0.1271.64 Safari/537.11',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                        'Accept-Encoding': 'none',
                        'Accept-Language': 'en-US,en;q=0.8',
                        'Connection': 'keep-alive'
                }
                r = requests.get(link)
                Image.open(BytesIO(r.content))
                req = urllib.request.Request(link, headers=headers)
                html = urllib.request.urlopen(req).read()
                profile_image = base64.encodestring(html)
                val = {
                    'image': profile_image,
                }
                return {'value': val}
        except:
            raise Warning(_("Please provide correct URL or check your image size.!"))


class QuestionFormulier(models.Model):
    _inherit = "question.formulier"

    web_url = fields.Char(string='Image URL', help='Automatically sanitized HTML contents', copy=False, translate=True)

    @api.onchange('web_url')
    def onchange_image(self):
        link = self.web_url
        try:
            if link:
                headers = {
                        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) ' 
                        'AppleWebKit/537.11 (KHTML, like Gecko) '
                        'Chrome/23.0.1271.64 Safari/537.11',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                        'Accept-Encoding': 'none',
                        'Accept-Language': 'en-US,en;q=0.8',
                        'Connection': 'keep-alive'
                }
                r = requests.get(link)
                Image.open(BytesIO(r.content))
                req = urllib.request.Request(link, headers=headers)
                html = urllib.request.urlopen(req).read()
                profile_image = base64.encodestring(html)
                val = {
                    'image': profile_image,
                }
                return {'value': val}
        except:
            raise Warning(_("Please provide correct URL or check your image size.!"))
