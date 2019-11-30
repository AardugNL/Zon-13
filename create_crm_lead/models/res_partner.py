# -*- encoding: utf-8 -*-

from odoo import models, fields, api


@api.model
def _lang_get(self):
    return self.env['res.lang'].get_installed()


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def default_get(self, fields):
        res = super(ResPartner, self).default_get(fields)
        res['lang'] = 'nl_NL'

        ir_model_data = self.env['ir.model.data']
        res['country_id'] = ir_model_data.get_object_reference('base', 'nl')[1]
        return res


class MailMessage(models.Model):
    _inherit = 'mail.message'

    company = fields.Char('Company Name')
