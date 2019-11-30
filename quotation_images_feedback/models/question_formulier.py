# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class QuestionFormulier(models.Model):
    """ Question Formulier Model """

    _name = "question.formulier"
    _inherit = ['mail.thread'] 
    _description = "Questions/Answers"
    _order = "id desc"

    name = fields.Char('Name', track_visibility='always')
    active = fields.Boolean(default=True)
    lead_id = fields.Many2one('crm.lead', string='Lead', readonly=True)
    image = fields.Binary(track_visibility='always')
    partner_id = fields.Many2one('res.partner', string="Customer")
    customer_type = fields.Selection(related='lead_id.customer_type', string="Question Type")
    state = fields.Selection([('concept', 'Concept'),
                            ('opportunity', 'Opportunity'),
                            ('opportunity_output', 'Opportunity Output'),
                            ('quotation', 'Quotation'),
                            ('quotation_output', 'Quotation Output'),
                            ('task', 'Task'),
                            ('task_output', 'Task Output'),
                            ('done', 'Done'),],
                             string='status', default='concept', required=True, track_visibility='always')
    street = fields.Char(track_visibility='always')
    street2 = fields.Char(track_visibility='always')
    zip = fields.Char(track_visibility='always')
    city = fields.Char(track_visibility='always')
    state_id = fields.Many2one("res.country.state", string='State', ondelete='restrict', track_visibility='always')
    country_id = fields.Many2one('res.country', string='Country', ondelete='restrict', track_visibility='always')

    phone = fields.Char(string='Phone', track_visibility='always')
    mobile = fields.Char('Mobile', track_visibility='always')
    time = fields.Datetime('Time of day', track_visibility='always')

    image_ids = fields.One2many('order.image', 'question_frm_id', track_visibility='always', string='Images')
    sale_number = fields.Integer(compute='_compute_quotation', string="Number of Quotations")
    order_ids = fields.One2many('sale.order', 'question_frm_id', string='Quotation')
    lead_number = fields.Integer(compute='_compute_quotation', string="Number of Lead")
    lead_ids = fields.One2many('crm.lead', 'question_frm_id', string='Opportunities')
    task_number = fields.Integer(compute='_compute_quotation', string="Number of Task")
    task_ids = fields.One2many('project.task', 'question_frm_id', string='Tasks')

    date_opportunity = fields.Date(string='Meeting Date')
    date_report = fields.Date(string='Report Date')

    video_ids = fields.One2many('order.video', 'question_frm_id', track_visibility='always', string='Video')
    document_ids = fields.One2many('order.document', 'question_frm_id', track_visibility='always', string="Document")

    def goto_website_form(self):
        return {
            'type': 'ir.actions.act_url',
            'url': '/question/formulier/'+str(self.id),
            'target': 'self',
        }

    def opportunity_stage(self):
        self.state = 'opportunity'

    def quotation_stage(self):
        self.state = 'quotation'

    def task_stage(self):
        self.state = 'task'

    @api.depends('order_ids')
    def _compute_quotation(self):
        for formulier in self:
            s_nbr = 0
            for order in formulier.order_ids:
                s_nbr += 1
            formulier.lead_number = len(formulier.lead_ids.ids) or 0
            formulier.task_number = len(formulier.task_ids.ids) or 0
            formulier.sale_number = s_nbr


    def online_pf_dictionary(self):
        """ online pf possible values"""

        user = self.env.user
        products = self.env['product.product'].sudo().search([])
        countries = self.env['res.country'].search([])
        values = {'question_frm_id': self,
                'countries': countries,
                'products': products,
                'user': user}
        return values

class OrderImage(models.Model):
    """ new module for add images in question.formulier"""

    _name = 'order.image'
    _description = 'Opportunity Images'

    name = fields.Char('Name')
    image = fields.Binary('Image', attachment=True)
    file_type = fields.Char('File Type')
    is_task = fields.Boolean('Is for Task')
    question_frm_id = fields.Many2one('question.formulier', 'Related Form', copy=True, readonly=True)

class OrderVideo(models.Model):
    """ new model for add videos in question.formulier"""

    _name = 'order.video'
    _description = 'Opportunity Videos'

    name = fields.Char('Name')
    video = fields.Binary('Video', attachment=True)
    file_type = fields.Char('File Type')
    is_task = fields.Boolean('Is for Task')
    question_frm_id = fields.Many2one('question.formulier', 'Related Form', copy=True, readonly=True)

class OrderDocument(models.Model):
    """ new model for add Documents in question.formulier"""

    _name = 'order.document'
    _description = 'Opportunity Documents'

    name = fields.Char('Name')
    file = fields.Binary('File', attachment=True)
    file_type = fields.Char('File Type')
    question_frm_id = fields.Many2one('question.formulier', 'Related Form', copy=True, readonly=True)
