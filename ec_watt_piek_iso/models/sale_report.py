from odoo import models, fields, api, tools



class SaleReport(models.Model):
    _inherit = "sale.report"

    ec_order_watt_piek = fields.Float(string="EC Order Watt Piek")
    ec_order_iso = fields.Float(string="EC Order ISO")

    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        fields['ec_order_watt_piek'] = ", sum(l.total_ec_watt_piek) as ec_order_watt_piek"
        fields['ec_order_iso'] = ",sum(l.total_ec_iso) as ec_order_iso"
        return super(SaleReport, self)._query(with_clause, fields, groupby, from_clause)


