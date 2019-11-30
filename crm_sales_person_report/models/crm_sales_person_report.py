# -*- coding: utf-8 -*-

from odoo import fields, models, tools

class CrmSalesPersonReport(models.Model):
    _name = "crm.sales.person.report"
    _description = "CRM Statistics"
    _auto = False

    quote = fields.Many2one('res.users', string='Quote')
    user_id = fields.Many2one('res.users', string='Sales Person')
    opportunity = fields.Many2one('res.users', string='Meeting')
    deal = fields.Many2one('res.users', string='Deal')
    work = fields.Many2one('res.users', string='Work')
    phone = fields.Many2one('res.users', string='Call')
    work_date = fields.Datetime(string='Work Date')
    deal_date = fields.Datetime(string='Deal Date')
    opportunity_date = fields.Datetime(string='Meeting Date')
    quote_date = fields.Datetime(string='Quote Date')
    phone_date = fields.Datetime(string='Call Date')
    user_by_total = fields.Integer(string='Total Created')
    deal_by_total = fields.Integer(string='Total Deal')
    opportunity_by_total = fields.Integer(string='Total Meeting')
    work_by_total = fields.Integer(string='Total Work')
    phone_by_total = fields.Integer(string='Total Call')
    quote_by_total = fields.Integer(string='Total Quote')
    
    def init(self):
        tools.drop_view_if_exists(self._cr, 'crm_sales_person_report')
        self._cr.execute("""CREATE OR REPLACE VIEW crm_sales_person_report AS (
                                                        SELECT
                                                        max(id) as id,
                                                        user_id as user_id,
                                                        quote_by as quote,
                                                        phone_by as phone,
                                                        deal_by as  deal,
                                                        work_by as work,
                                                        opportunity_by as opportunity,
                                                        deal_date as deal_date,
                                                        work_date as work_date,
                                                        phone_date as phone_date,
                                                        opportunity_date as opportunity_date,
                                                        quote_date as quote_date,
                                                        count(user_id) as user_by_total,
                                                        count(quote_by) as quote_by_total,
                                                        count(phone_by) as phone_by_total,
                                                        count(deal_by) as  deal_by_total,
                                                        count(work_by) as work_by_total,
                                                        count(opportunity_by) as opportunity_by_total
                                                        FROM
                                                        crm_lead 
                                                        WHERE type = 'opportunity'
                                                        GROUP BY 
                                                        id,
                                                        user_id,
                                                        quote_by,
                                                        phone_by,
                                                        deal_by,
                                                        work_by,
                                                        deal_date, 
                                                        work_date,
                                                        phone_date,
                                                        opportunity_date,
                                                        quote_date
)""" )
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

