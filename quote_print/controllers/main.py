# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

import re

from odoo import http
from odoo.http import request
from odoo.addons.sale.controllers.portal import CustomerPortal


class customSaleQuote(CustomerPortal):

    @http.route(['/my/orders/<int:order_id>'], type='http', auth="public", website=True)
    def portal_order_page(self, order_id, report_type=None, access_token=None, message=False, download=False, **kw):
        try:
            order_sudo = self._document_check_access('sale.order', order_id, access_token=access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')

        if report_type in ('html', 'pdf', 'text'):
            return self._show_report(model=order_sudo, report_type='pdf', report_ref='quote_print.report_web_quotation_custom', download=download)
        result = super(customSaleQuote, self).portal_order_page(order_id, report_type=report_type, access_token=access_token, message=message, download=download, **kw)
        if access_token:
            order = request.env['sale.order'].sudo().search([('id', '=', order_id), ('access_token', '=', access_token)])
        else:
            order = request.env['sale.order'].search([('id', '=', order_id)])

        if report_type == 'pdf':
            return result
        if not order:
            return result

        if hasattr(result, 'render'):
            renderedResult = result.render()
        elif hasattr(result, 'replace'):
            renderedResult = result
        else:
            return result

        variables = re.findall(b'\${custom:.*?}', renderedResult)

        if not variables:
            return result

        object = order
        for variable in variables:
            value = eval(variable[9:-1])
            if isinstance(value, (int, float, list, tuple, dict)):
                try:
                    # There are uncertain possible data. So making generic and ignore issue.
                    try:
                        value = str(value).encode("utf-8").decode("utf-8")
                    except:
                        value = str(value).decode("utf-8")
                except:
                    print ('Invalid Data')
                    value = u''
            renderedResult = renderedResult.replace(variable, value.encode('utf-8'))
        return result
