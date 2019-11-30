# -*- coding: utf-8 -*-

import os
import re
import base64
import tempfile
from contextlib import closing
from PyPDF2 import PdfFileWriter, PdfFileReader
from logging import getLogger

from odoo import api, fields, models
from odoo.addons.quote_print.caretutils import listutils

_logger = getLogger(__name__)


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    website_desc_footer = fields.Html('Template Footer', translate=True)
    website_desc_footer_bellow = fields.Html('Template Footer Bellow', translate=True)
    show_only_total = fields.Boolean(
        string='Show Only Total', translate=True)
    cover_image = fields.Binary("Cover Image", store=True)
    close_image = fields.Binary('Closing Image')

    def action_quotation_send(self):
        # TODO: Dhaval
        ''' this method use to set email template which is set in Quotation Template  '''
        res = super(SaleOrderInherit, self).action_quotation_send()
        if self.sale_order_template_id and self.sale_order_template_id.mail_template_id:
            res['context']['default_template_id'] = self.sale_order_template_id.mail_template_id.id or False
        return res

    @api.onchange('sale_order_template_id')
    def onchange_sale_order_template_id(self):
        res = super(SaleOrderInherit, self).onchange_sale_order_template_id()
        if not self.sale_order_template_id:
            return res
        template = self.sale_order_template_id.with_context(lang=self.partner_id.lang)
        self.update({
            'website_desc_footer': template.website_desc_footer,
            'website_desc_footer_bellow': template.website_desc_footer_bellow,
            'cover_image': template.cover_image,
            'close_image': template.close_image
        })
        return res

    def get_quote_print_pdf(self):
        return self.env.ref('quote_print.report_web_quotation_custom').report_action(self)


class mailComposeMessage(models.TransientModel):
    _inherit = 'mail.compose.message'

    @api.onchange('template_id')
    def onchange_template_id_wrapper(self):
        """owrwrite this mehod to display SO template's pdf attachment in mail
           compose message wizard and send that attachment with mail."""
        result = super(mailComposeMessage, self).onchange_template_id_wrapper()
        if self.env.context['active_model'] == 'sale.order':
            order = self.env['sale.order'].browse(self.env.context['active_id'])
            if order and order.sale_order_template_id and order.sale_order_template_id.pdf_attachment:
                res = self._cr.execute('''
                    SELECT id
                    FROM ir_attachment
                    WHERE res_model = 'sale.order.template'
                      AND res_id = %s
                      AND res_field = 'pdf_attachment'
                    ''' % (order.sale_order_template_id.id))
                res = self._cr.fetchall()
                for attachment in res:
                    if attachment:
                        att_rec = self.env['ir.attachment'].browse(attachment[0])
                        if att_rec:
                            if att_rec.name.find('.')==-1:
                                att_rec.write({'name': att_rec.name + '.pdf'})
                            if not att_rec.datas_fname:
                                att_rec.write({'datas_fname': order.sale_order_template_id.file_name_pdf})
                new_attachment_ids = []
                for attachment_id in self.attachment_ids:
                    new_attachment_ids.append(attachment_id.id)
                new_attachment_ids.append(res[0][0])
                self.attachment_ids = [(6, 0, new_attachment_ids)]
        return result


class SaleQuoteTemplateInh(models.Model):
    _inherit = 'sale.order.template'

    website_desc_footer = fields.Html('Template Footer', translate=True)
    website_desc_footer_bellow = fields.Html('Template footer', translate=True)
    cover_image = fields.Binary("Cover Image", attachment=True)
    file_name_cover = fields.Char('File Name')
    cover_image_pdf = fields.Binary("Cover Image Pdf", attachment=True)
    report_layout = fields.Selection([
         ('address_only', 'First Page Address Only'),
         ('no_extra_space', 'Start Content From First Page')],
         string='Report Layout')
    file_name_cover_pdf = fields.Char('Pdf File Name')
    cover_height = fields.Integer(string="Cover Image Height", default=1031)
    isfooteradrsimg_first_page = fields.Boolean(
        string="Remove Footer",
        help="Show footer address image on first\
        page when rest pages don't have footer")
    close_image = fields.Binary('Closing Image', attachment=True)
    close_height = fields.Integer(string="Closing Image Height", default=1031)
    file_name_close = fields.Char('Close File Name')
    close_image_pdf = fields.Binary("Close Image Pdf", attachment=True)
    file_name_close_pdf = fields.Char('Pdf File name')
    header_image = fields.Binary("Header Image")
    file_name_header = fields.Char('Header File name')
    footer_image = fields.Binary("Footer Image")
    file_name_footer = fields.Char('Footer File Name')
    pdf_attachment = fields.Binary('PDF Attachment', attachment=True)
    file_name_pdf = fields.Char('PDF File Name')
    hide_pricing_tab = fields.Boolean(string='Hide Pricing Tab')

    @api.model
    def create(self, values):
        result = super(SaleQuoteTemplateInh, self).create(values)
        if result.cover_image:
            result.generate_pdf()
        if result.close_image:
            result.generate_pdf()
        return result

    def write(self, values):
        result = super(SaleQuoteTemplateInh, self).write(values)
        if self.cover_image and values.get('cover_height'):
            self.generate_pdf()
        if values.get('cover_image'):
            self.generate_pdf()

        if self.close_image and values.get('close_height'):
            self.generate_pdf()
        if values.get('close_image'):
            self.generate_pdf()
        return result

    def generate_pdf(self):
        if not self.cover_image:
            self.cover_image_pdf = None
            self.file_name_cover_pdf = None
        else:
            #pdf = self.env['ir.actions.report'].sudo()._get_report_from_name('quote_print.report_quote_cover')
            #pdf_bin, _ = pdf.with_context(snailmail_layout=True).render_qweb_pdf(self.id)
            reportAct = self.env.ref('quote_print.report_web_quote_cover')
            if reportAct:
                pdf_bin, _ = reportAct.render_qweb_pdf(docids=self.id)
                self.cover_image_pdf = base64.b64encode(pdf_bin)
                self.file_name_cover_pdf = (self.file_name_cover.split('.')[0] or 'cover') + '.pdf'
        if not self.close_image:
            self.close_image_pdf = None
            self.file_name_close_pdf = None
        else:
            # closePdf = self.env['ir.actions.report'].sudo()._get_report_from_name('quote_print.report_quote_close')
            # closePdf_bin, _ = closePdf.with_context(snailmail_layout=True).render_qweb_pdf(self.id)
            reportCloseAct = self.env.ref('quote_print.report_web_quote_close')
            if reportCloseAct:
                closepdf_bin, _ = reportCloseAct.render_qweb_pdf(docids=self.id)
                self.close_image_pdf = base64.b64encode(closepdf_bin)
                self.file_name_close_pdf = (self.file_name_close.split('.')[0] or 'close') + '.pdf'


class IrActionsReportInh(models.Model):
    _inherit = 'ir.actions.report'

    @api.model
    def render_qweb_html(self, docids, data=None):
        html = super(IrActionsReportInh, self).render_qweb_html(docids, data=data)
        if (self.model != 'sale.order' and
            self.report_name != 'quote_print.report_web_quotation_custom'):
            return html

        variables = re.findall(b'\${custom:.*?}', html[0])
        if not variables:
            return html
        lst = list(html)
        for i, variChunk in enumerate(listutils.chunks(variables, len(variables) / len(docids))):
            docId = docids[i]
            object = self.env['sale.order'].browse(docId)
            for variable in variChunk:
                value = eval(variable[9:-1])
                if isinstance(value, (int, float, list, tuple, dict)):
                    try:
                        # There are uncertain possible data. So making generic and ignore issue.
                        try:
                            value = str(value).encode("utf-8").decode("utf-8")
                        except:
                            value = str(value).decode("utf-8")
                    except:
                        value = u''
                lst[0] = lst[0].replace(variable, value.encode('utf-8'), 1)
        return tuple(lst)

    def _merge_pdf(self, documents):
        """Merge PDF files into one."""
        writer = PdfFileWriter()
        streams = []
        try:
            for document in documents:
                pdfreport = open(document, 'rb')
                streams.append(pdfreport)
                reader = PdfFileReader(pdfreport)
                for page in range(0, reader.getNumPages()):
                    writer.addPage(reader.getPage(page))

            merged_file_fd, merged_file_path = tempfile.mkstemp(
                suffix='.pdf', prefix='report.merged.tmp.')
            with closing(os.fdopen(merged_file_fd, 'wb')) as merged_file:
                writer.write(merged_file)
        finally:
            for stream in streams:
                try:
                    stream.close()
                except Exception:
                    pass
        return merged_file_path

    def render_qweb_pdf(self, docids, data=None):
        """This method generates and returns pdf version with background of a report.
        """
        temporary_files = []
        pdf = super(IrActionsReportInh, self).render_qweb_pdf(docids, data=data)
        if (self.model != 'sale.order' and
            self.report_name != 'quote_print.custom_web_quote_print'):
            return pdf
        soId = docids[0] if isinstance(docids, list) else docids
        so = self.env['sale.order'].browse(soId)
        if not so.sale_order_template_id:
            return pdf
        if so.sale_order_template_id.isfooteradrsimg_first_page:
            self.paperformat_id.write({'margin_bottom': 23})
        else:
            self.paperformat_id.write({'margin_bottom': 53})

        cover_image = so.sale_order_template_id.cover_image
        cover_image_pdf = so.sale_order_template_id.cover_image_pdf
        if (cover_image and cover_image_pdf and (not so.sale_order_template_id.report_layout 
            or so.sale_order_template_id.report_layout in ['address_only','no_extra_space'])):

            writer = PdfFileWriter()
            streams = []
            try:
                report_fd, report_path = tempfile.mkstemp(
                    suffix='.pdf', prefix='report.tmp.')
                temporary_files.append(report_path)
                with closing(os.fdopen(report_fd, 'wb')) as repo:
                    repo.write(pdf[0])
            finally:
                for stream in streams:
                    try:
                        stream.close()
                    except Exception:
                        pass

            cover_image_pdf = base64.decodestring(cover_image_pdf)
            cover_fd, cover_path = tempfile.mkstemp(
                suffix='.pdf', prefix='report.tmp.')
            temporary_files.append(cover_path)
            with closing(os.fdopen(cover_fd, 'wb')) as repo:
                repo.write(cover_image_pdf)

            mergeFile = self._merge_pdf([cover_path, report_path])
            with open(mergeFile, 'rb') as pdfdocument:
                pdf = pdfdocument.read(), 'pdf'

        close_image = so.sale_order_template_id.close_image
        close_image_pdf = so.sale_order_template_id.close_image_pdf
        if close_image and close_image_pdf:
            writer = PdfFileWriter()
            streams = []
            try:
                report_fd, report_path = tempfile.mkstemp(
                    suffix='.pdf', prefix='report.tmp.')
                temporary_files.append(report_path)
                with closing(os.fdopen(report_fd, 'wb')) as repo:
                    repo.write(pdf[0])
            finally:
                for stream in streams:
                    try:
                        stream.close()
                    except Exception:
                        pass

            close_image_pdf = base64.decodestring(close_image_pdf)
            close_fd, close_path = tempfile.mkstemp(
                suffix='.pdf', prefix='report.tmp.')
            temporary_files.append(close_path)
            with closing(os.fdopen(close_fd, 'wb')) as repo:
                repo.write(close_image_pdf)

            mergeFile = self._merge_pdf([report_path, close_path])
            with open(mergeFile, 'rb') as pdfdocument:
                pdf = pdfdocument.read(), 'pdf'

            # Manual cleanup of the temporary files
        for temporary_file in temporary_files:
            try:
                os.unlink(temporary_file)
            except (OSError, IOError):
                _logger.error('Error when trying to remove file %s' % temporary_file)

        return pdf

    @api.model
    def _run_wkhtmltopdf(
            self,
            bodies,
            header=None,
            footer=None,
            landscape=False,
            specific_paperformat_args=None,
            set_viewport_size=False):

        if self.report_name == 'quote_print.custom_web_quote_print':
            set_viewport_size = True
        res = super(IrActionsReportInh, self)\
            ._run_wkhtmltopdf(
                bodies,
                header,
                footer,
                landscape,
                specific_paperformat_args=specific_paperformat_args,
                set_viewport_size=set_viewport_size
            )
        return res

class CompanyInheritQuote(models.Model):
    _inherit = 'res.company'

    footer_address_image = fields.Binary('Footer Address Image', attachment=True)
    file_name_footer_address = fields.Char()
    footer_no_address_image = fields.Binary('Footer Without Address Image', attachment=True)
    file_name_footer_no_address = fields.Char()
    footeradrs_first_page_img = fields.Binary(
        'Footer Address Image First Page', attachment=True)
    file_name_footeradrsfirstpage = fields.Char()
