# -*- coding: utf-8 -*-

import logging
from odoo import fields, http, _, SUPERUSER_ID
from odoo.http import request
from odoo.addons.quotation_images_feedback.controllers.main import WebFormulier
import json
import base64

_logger = logging.getLogger(__name__)

class WebFormulier(WebFormulier):

    @http.route(['/question/formulier/submit/<int:question_frm_id>/<string:model_name>'], type='http',
                auth='user', methods=['POST'], website=True)
    def question_formulier_submit(self,question_frm_id,model_name, **kwargs):
        """ Project Formulier web form submit """

        if question_frm_id:
            if kwargs.get('solar_product'):
                kwargs.update({'solar_product': int(kwargs.get('solar_product'))})
            if kwargs.get('converter_product'):
                kwargs.update({'converter_product': int(kwargs.get('converter_product'))})
            if kwargs.get('flat_roof_product'):
                kwargs.update({'flat_roof_product': int(kwargs.get('flat_roof_product'))})
            if kwargs.get('slanted_roof_product'):
                kwargs.update({'slanted_roof_product': int(kwargs.get('slanted_roof_product'))})
            if kwargs.get('stekkers_product'):
                kwargs.update({'stekkers_product': int(kwargs.get('stekkers_product'))})
            if kwargs.get('remain_material'):
                kwargs.update({'remain_material': int(kwargs.get('remain_material'))})
            if kwargs.get('vat_refund_product'):
                kwargs.update({'vat_refund_product': int(kwargs.get('vat_refund_product'))})
            if kwargs.get('optimiser_product'):
                kwargs.update({'optimiser_product': int(kwargs.get('optimiser_product'))})
            if kwargs.get('discount_product'):
                kwargs.update({'discount_product': int(kwargs.get('discount_product'))})
            if kwargs.get('quote_template_id'):
                kwargs.update({'quote_template_id': int(kwargs.get('quote_template_id'))})
            if kwargs.get('solar_type'):
                kwargs.update({'solar_type': [(6,0,[int(i) for i in list(kwargs.get('solar_type')) if i.isdigit()])]})
        return super(WebFormulier, self).question_formulier_submit(question_frm_id,model_name,**kwargs)

    @http.route(['/formulier/quote_infos'], type='json', auth="user", methods=['POST'], website=True)
    def quote_infos(self, energy=0.0, quote_type=None, roof=None, solar_type=None, product_id=0, **kw):
        """ Send Required data to Quote PV tab"""

        productObj = request.env['product.product'].sudo()
        solarP = productObj
        FlatRoofProducts = request.env['product.product'].sudo()
        SlantedRoofProducts = request.env['product.product'].sudo()
        if solar_type:
            solarP = productObj.search([
                ('product_type', '=', 'Solar Panel'),
                ('solar_type','in',[int(sol) for sol in solar_type])], order='priority')
        converterProducts = productObj.search([
            '&', ('min_product_range', '<=', energy),
            ('max_product_range', '>=', energy),
            ('product_type', '=', 'Converter')], order='priority')
        if str(roof) in ['Flat Roof', 'Mix Roof']:
            FlatRoofProducts = productObj.search([
                ('product_type', '=', 'Flat Roof')], order='priority')
        if str(roof) in ['Slanted Roof', 'Mix Roof']:
            SlantedRoofProducts = productObj.search([
                ('product_type', '=', 'Slanted Roof')], order='priority')
        energy_wat_piek = 0
        selectProduct = productObj
        optimiserProducts = productObj
        if product_id:
            selectProduct = productObj.browse(product_id)
            energy_wat_piek = selectProduct.ec_watt_piek
            if selectProduct.product_type == 'Converter' and selectProduct.product_brand:
                optimiserProducts = productObj.search([
                            ('product_type', '=', 'Optimisers'),
                            ('product_brand','=', selectProduct.product_brand.id)],
                             order='priority')
        return dict(
            converterProducts=[(cp.id, cp.name, cp.list_price) for cp in converterProducts],
            optimiserProducts = [(op.id, op.name, op.list_price) for op in optimiserProducts],
            FlatRoofProducts=[(frp.id, frp.name) for frp in FlatRoofProducts],
            SlantedRoofProducts=[(srp.id, srp.name) for srp in SlantedRoofProducts],
            energy_wat_piek=energy_wat_piek,
            solarProduct=[(sp.id, sp.name, sp.list_price) for sp in selectProduct],
            solarP=[(sp.id, sp.name, sp.ec_watt_piek, sp.list_price) for sp in solarP],
        )

    @http.route(['/formulier/quote_create'], type='json', auth="user", methods=['POST'], website=True)
    def quote_create(self, quoteData, que_id, eval_quote,**kw):
        """ Create quotation from PF online page"""

        Product = request.env['product.product'].sudo()
        ir_values = request.env['ir.config_parameter'].sudo()
        hours,hours_cost,hours_sales=0,0,0
        range_amount = 0
        if quoteData['is_discount_2'] == 'ja':
            if quoteData['amount_range']:
                 get_amount = int(quoteData['amount_range'])
                 if get_amount > 0:
                    range_amount = get_amount / 2
            # if quoteData['amount_range'] == 'Hoog':
            #     range_amount = ir_values.get_default('formulier.config.settings', 'high_range')
            #     if range_amount > 0:
            #         range_amount = range_amount / 2
            # elif quoteData['amount_range'] == 'Middel':
            #     range_amount = ir_values.get_default('formulier.config.settings', 'middle_range')
            #     if range_amount > 0:
            #         range_amount = range_amount / 2
            # elif quoteData['amount_range'] == 'Basis':
            #     range_amount = ir_values.get_default('formulier.config.settings', 'basic_range')
            #     if range_amount > 0:
            #         range_amount = range_amount / 2
            # elif quoteData['amount_range'] == 'Laag':
            #     range_amount = ir_values.get_default('formulier.config.settings', 'low_range')
            #     if range_amount > 0:
            #         range_amount = range_amount / 2

        if quoteData['installation_time'] == '4 Hours':
            hours = 4
            hours_cost = ir_values.get_param('formulier_type_3.cost_4_hours')
            hours_sales = ir_values.get_param('formulier_type_3.sale_4_hours')
        elif quoteData['installation_time'] == '8 Hours':
            hours = 8
            hours_cost = ir_values.get_param('formulier_type_3.cost_8_hours')
            hours_sales = ir_values.get_param('formulier_type_3.sale_8_hours')
        elif quoteData['installation_time'] == '12 Hours':
            hours = 12
            hours_cost = ir_values.get_param('formulier_type_3.cost_12_hours')
            hours_sales = ir_values.get_param('formulier_type_3.sale_12_hours')
        elif quoteData['installation_time'] == '16 Hours':
            hours = 16
            hours_cost = ir_values.get_param('formulier_type_3.cost_16_hours')
            hours_sales = ir_values.get_param('formulier_type_3.sale_16_hours')
        elif quoteData['installation_time'] == '24 Hours':
            hours = 24
            hours_cost = ir_values.get_param('formulier_type_3.cost_24_hours')
            hours_sales = ir_values.get_param('formulier_type_3.sale_24_hours')
        elif quoteData['installation_time'] == '30 Hours':
            hours = 30
            hours_cost = ir_values.get_param('formulier_type_3.cost_30_hours')
            hours_sales = ir_values.get_param('formulier_type_3.sale_30_hours')
        elif quoteData['installation_time'] == '32 Hours':
            hours = 32
            hours_cost = ir_values.get_param('formulier_type_3.cost_32_hours')
            hours_sales = ir_values.get_param('formulier_type_3.sale_32_hours')
        elif quoteData['installation_time'] == '36 Hours':
            hours = 36
            hours_cost = ir_values.get_param('formulier_type_3.cost_36_hours')
            hours_sales = ir_values.get_param('formulier_type_3.sale_36_hours')
        elif quoteData['installation_time'] == '40 Hours':
            hours = 40
            hours_cost = ir_values.get_param('formulier_type_3.cost_40_hours')
            hours_sales = ir_values.get_param('formulier_type_3.sale_40_hours')
        user = request.env.user
        if eval_quote:
            SaleOrder = request.env['sale.order.temp'].sudo()
            SaleOrderLine = request.env['sale.order.line.temp'].sudo()
        else:
            SaleOrder = request.env['sale.order'].sudo()
            SaleOrderLine = request.env['sale.order.line'].sudo()
        if que_id and quoteData:
            que_id = request.env['question.formulier'].browse(int(que_id))
            if que_id.partner_id:
                # product_id = request.env['product.product'].browse(int(product))
                quote = SaleOrder.create({
                        'partner_id': que_id.partner_id.id,
                        'question_frm_id': que_id.id,
                        'opportunity_id': que_id.lead_id and que_id.lead_id.id,
                        'sale_order_template_id': quoteData['template_id'],
                    })
                quote.onchange_sale_order_template_id()
                quote.fill_drawing_images()
                if quoteData['vat_id']:
                    SaleOrderLine.create({
                        'order_id': quote.id,
                        'product_id': quoteData['vat_id'],
                        'product_uom_qty': 1,
                        'discount': 100,
                    })
                if quoteData['solar_id']:
                    SaleOrderLine.create({
                        'order_id': quote.id,
                        'product_id': quoteData['solar_id'],
                        'product_uom_qty': quoteData['solar_qty'],
                        'price_unit': quoteData['panel_price'],
                    })
                if quoteData['is_optimizer'] == 'ja' and quoteData['optimiser_id']:
                    SaleOrderLine.create({
                        'order_id': quote.id,
                        'product_id': quoteData['optimiser_id'],
                        'product_uom_qty': quoteData['optimiser_qty'],
                        'price_unit': quoteData['optimisers_price'],
                    })
                if quoteData['is_converter'] == 'ja' and quoteData['converter_id']:
                    SaleOrderLine.create({
                        'order_id': quote.id,
                        'product_id': quoteData['converter_id'],
                        'product_uom_qty': quoteData['converter_qty'],
                        'price_unit': quoteData['converter_price'],
                    })
                if quoteData['roof'] in ['Flat Roof','Mix Roof'] and quoteData['flat_roof_id']:
                    SaleOrderLine.create({
                        'order_id': quote.id,
                        'product_id': quoteData['flat_roof_id'],
                        'product_uom_qty': quoteData['flat_roof_qty'],
                    })
                if quoteData['roof'] in ['Slanted Roof','Mix Roof'] and quoteData['slanted_roof_id']:
                    SaleOrderLine.create({
                        'order_id': quote.id,
                        'product_id': quoteData['slanted_roof_id'],
                        'product_uom_qty': quoteData['slanted_roof_qty'],
                    })
                if quoteData['stekkers_id']:
                    SaleOrderLine.create({
                        'order_id': quote.id,
                        'product_id': quoteData['stekkers_id'],
                        'product_uom_qty': 1,
                    })
                if quoteData['is_discount'] == 'ja' and quoteData['discount_id']:
                    SaleOrderLine.create({
                        'order_id': quote.id,
                        'product_id': quoteData['discount_id'],
                        'product_uom_qty': quoteData['discount_qty'],
                    })
                if quoteData['installation_time']:
                    installation_product = Product.search([('name', 'ilike', 'Montage kosten')], limit=1)
                    if installation_product:
                        SaleOrderLine.create({
                            'order_id': quote.id,
                            'product_id': installation_product.id,
                            'product_uom_qty': 1,
                            'price_unit': hours_sales + range_amount,
                            'purchase_price': hours_cost,
                        })
                if quoteData['material_id']:
                    material_product = Product.browse(quoteData['material_id'])
                    SaleOrderLine.create({
                        'order_id': quote.id,
                        'product_id': material_product.id,
                        'product_uom_qty': 1,
                        'price_unit': material_product.lst_price + range_amount,
                    })
                if quoteData['installation_time']:
                    task_product = Product.search([('name', 'ilike', 'Projectbegeleiding zonnepanelen (intern)')], limit=1)
                    if task_product:
                        SaleOrderLine.create({
                            'order_id': quote.id,
                            'product_id': task_product.id,
                            'product_uom_qty': hours,
                        })
                if eval_quote:
                    # currency = quote.currency_id or quote.company_id.currency_id
                    if not user.show_score:
                        return [str(quote.amount_untaxed)]
                    else:
                        margin_per = '{0:.2f}'.format(quote.margin / 100)
                        return [str(margin_per)+' %','€ '+ str(quote.amount_untaxed)]
                    
                else:
                    return quote.preview_sale_order()
        return True
