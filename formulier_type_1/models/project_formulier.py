# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
import re


class SaleOrder(models.Model):
    """ Question Formulier Tab """

    _inherit = "sale.order"

    @api.model
    def fill_drawing_images(self):
        res = super(SaleOrder, self).fill_drawing_images()
        footer = ""
        description = ""
        imgDict = {}
        if self.website_description:
            description = self.website_description.encode('utf-8')
        # if self.website_desc_footer:
        #     footer = self.website_desc_footer.encode('utf-8')

        if description:# or footer:
            if self.sale_order_template_id :
                # and self.sale_order_template_id.pdf_attachment and self.sale_order_template_id.file_name_pdf:
                # imgDict.update({' <a href="#" id="quotation_template_pdf" target="_blank">':
                #                 ' <a href="/web/content?model=sale.order.template&field=pdf_attachment&id='+str(self.sale_order_template_id.id)+'&filename='+self.sale_order_template_id.file_name_pdf+'&download=true" id="quotation_template_pdf" target="_blank">'})

                commonKey = '<img class="card-img-top img-border-style" src="/formulier_type_1/static/src/images/blank_image.jpg" alt="Odoo - Sample 1 for three columns"'
                commonVal = '<img class="card-img-top img-border-style" src=/web/image/question.formulier/' + str(self.question_frm_id.id)
                alt = 'alt="Odoo - Sample 1 for three columns"'

                # 6 image snippet and 1 main image
                if self.question_frm_id.plattegrond_img:
                    imgDict.update({'%s id="f_map">' % (commonKey): commonVal + '/plattegrond_img' +' '+ alt + ' ' +'id="f_map"/>'})
                    imgDict.update({'<img class="img img-fluid one_image_height_300" src="/formulier_type_1/static/src/images/blank_image.jpg" alt="Pallateground Image" id="plattegrond_img_id">':
                        '<img class="img img-fluid one_image_height_300" src=/web/image/question.formulier/'+ str(self.question_frm_id.id) + '/plattegrond_img' + ' ' + 'alt="Pallateground Image" id="plattegrond_img_id">'})
                if self.question_frm_id.fundering_img:
                    imgDict.update({'%s id="f_foundation">' % (commonKey): commonVal + '/fundering_img' +' '+ alt + ' ' +'id="f_foundation"/>'})
                    imgDict.update({'<img class="img img-fluid" src="/formulier_type_1/static/src/images/blank_image.jpg" alt="Sondering Image" id="fundering_img_id">':
                        '<img class="img img-fluid" src=/web/image/question.formulier/'+ str(self.question_frm_id.id) + '/fundering_img' + ' ' + 'alt="Sondering Image" id="fundering_img_id">'})
                if self.question_frm_id.blueprint_img:
                    imgDict.update({'%s id="f_blue_print">' % (commonKey): commonVal + '/blueprint_img' +' '+ alt + ' ' +'id="f_blue_print"/>',})
                    imgDict.update({'<img class="img img-fluid one_image_height_300" src="/formulier_type_1/static/src/images/blank_image.jpg" alt="Bouwtekening Image" id="blueprint_img_id">':
                        '<img class="img img-fluid one_image_height_300" src=/web/image/question.formulier/'+ str(self.question_frm_id.id) + '/blueprint_img' + ' ' + 'alt="Bouwtekening Image" id="blueprint_img_id">'})
                if self.question_frm_id.lot_img:
                    imgDict.update({'%s id="f_lot">' % (commonKey): commonVal + '/lot_img' +' '+ alt + ' ' +'id="f_lot"/>',})
                    imgDict.update({'<img class="img img-fluid one_image_height_300" src="/formulier_type_1/static/src/images/blank_image.jpg" alt="Kavel Image" id="lot_img_id">':
                        '<img class="img img-fluid one_image_height_300" src=/web/image/question.formulier/'+ str(self.question_frm_id.id) + '/lot_img' + ' ' + 'alt="Kavel Image" id="lot_img_id">'})
                if self.question_frm_id.extra_drawing_1_img:
                    imgDict.update({'%s id="f_extra_Drawing_1">' % (commonKey): commonVal + '/extra_drawing_1_img' +' '+ alt + ' ' +'id="f_extra_Drawing_1"/>',})
                    imgDict.update({'<img class="img img-fluid one_image_height_300" src="/formulier_type_1/static/src/images/blank_image.jpg" alt="Extra tekening 1 Image" id="extra_drawing_1_img_id">':
                        '<img class="img img-fluid one_image_height_300" src=/web/image/question.formulier/'+ str(self.question_frm_id.id) + '/extra_drawing_1_img' + ' ' + 'alt="Extra tekening 1 Image" id="extra_drawing_1_img_id">'})
                if self.question_frm_id.extra_drawing_2_img:
                    imgDict.update({'%s id="f_extra_Drawing_2">' % (commonKey): commonVal + '/extra_drawing_2_img' +' '+ alt + ' ' +'id="f_extra_Drawing_2"/>'})
                    imgDict.update({'<img class="img img-fluid one_image_height_300" src="/formulier_type_1/static/src/images/blank_image.jpg" alt="Extra tekening 2 Image" id="extra_drawing_2_img_id">':
                        '<img class="img img-fluid one_image_height_300" src=/web/image/question.formulier/'+ str(self.question_frm_id.id) + '/extra_drawing_2_img' + ' ' + 'alt="Extra tekening 2 Image" id="extra_drawing_2_img_id">'})
                if self.question_frm_id.image:
                    bannerKey = '<img src="/formulier_type_1/static/src/images/blank_image.jpg" class="img img-fluid" alt="Project Formulier" id="level_measurement_img">' 
                    imgDict.update({bannerKey:
                        '<img class="img img-fluid" src=/web/image/question.formulier/'+ str(self.question_frm_id.id) + '/image' + ' ' + 'alt="Project Formulier" id="level_measurement_img">'})

                # 8 image snippet
                if self.question_frm_id.image_1:
                    imgDict.update({'<img class="card-img-top img-height-65" src="/formulier_type_1/static/src/images/blank_image.jpg" alt="Odoo - Sample 1 for three columns" id="f_image_1">':
                                    '<img class="card-img-top img-height-65" src=/web/image/question.formulier/' + str(self.question_frm_id.id) + '/image_1' + ' ' + ' alt="Odoo - Sample 1 for three columns" id="f_image_1"/>'})
                if self.question_frm_id.image_2:
                    imgDict.update({'<img class="card-img-top img-height-65" src="/formulier_type_1/static/src/images/blank_image.jpg" alt="Odoo - Sample 2 for three columns" id="f_image_2">':
                                    '<img class="card-img-top img-height-65" src=/web/image/question.formulier/' + str(self.question_frm_id.id) + '/image_2' + ' ' + ' alt="Odoo - Sample 2 for three columns" id="f_image_2"/>'})
                if self.question_frm_id.image_3:
                    imgDict.update({'<img class="card-img-top img-height-65" src="/formulier_type_1/static/src/images/blank_image.jpg" alt="Odoo - Sample 3 for three columns" id="f_image_3">':
                                    '<img class="card-img-top img-height-65" src=/web/image/question.formulier/' + str(self.question_frm_id.id) + '/image_3' + ' ' + ' alt="Odoo - Sample 3 for three columns" id="f_image_3"/>'})
                if self.question_frm_id.image_4:
                    imgDict.update({'<img class="card-img-top img-height-65" src="/formulier_type_1/static/src/images/blank_image.jpg" alt="Odoo - Sample 3 for three columns" id="f_image_4">':
                                    '<img class="card-img-top img-height-65" src=/web/image/question.formulier/' + str(self.question_frm_id.id) + '/image_4' + ' ' + ' alt="Odoo - Sample 3 for three columns" id="f_image_4"/>'})
                if self.question_frm_id.image_5:
                    imgDict.update({'<img class="card-img-top img-height-65" src="/formulier_type_1/static/src/images/blank_image.jpg" alt="Odoo - Sample 1 for three columns" id="f_image_5">':
                                    '<img class="card-img-top img-height-65" src=/web/image/question.formulier/' + str(self.question_frm_id.id) + '/image_5' + ' ' + ' alt="Odoo - Sample 1 for three columns" id="f_image_5"/>'})
                if self.question_frm_id.image_6:
                    imgDict.update({'<img class="card-img-top img-height-65" src="/formulier_type_1/static/src/images/blank_image.jpg" alt="Odoo - Sample 2 for three columns" id="f_image_6">':
                                    '<img class="card-img-top img-height-65" src=/web/image/question.formulier/' + str(self.question_frm_id.id) + '/image_6' + ' ' + ' alt="Odoo - Sample 2 for three columns" id="f_image_6"/>'})
                if self.question_frm_id.image_7:
                    imgDict.update({'<img class="card-img-top img-height-65" src="/formulier_type_1/static/src/images/blank_image.jpg" alt="Odoo - Sample 3 for three columns" id="f_image_7">':
                                    '<img class="card-img-top img-height-65" src=/web/image/question.formulier/' + str(self.question_frm_id.id) + '/image_7' + ' ' + ' alt="Odoo - Sample 3 for three columns" id="f_image_7"/>'})
                if self.question_frm_id.image_8:
                    imgDict.update({'<img class="card-img-top img-height-65" src="/formulier_type_1/static/src/images/blank_image.jpg" alt="Odoo - Sample 3 for three columns" id="f_image_8">':
                                    '<img class="card-img-top img-height-65" src=/web/image/question.formulier/' + str(self.question_frm_id.id) + '/image_8' + ' ' + ' alt="Odoo - Sample 3 for three columns" id="f_image_8"/>'})

                # Situatie snippet
                if self.question_frm_id.house_info:
                    imgDict.update({'<p id="g_s_houseinfo_new_value" class="o_default_snippet_text">Double click an icon to replace it with one of your choice.</p>':
                                    '<p id="g_s_houseinfo_new_value" class="o_default_snippet_text">'+str(self.question_frm_id.house_info)+'</p>'})
                if self.question_frm_id.goal_owner:
                    imgDict.update({'<p id="g_s_goal_owner_new_value" class="o_default_snippet_text">Double click an icon to replace it with one of your choice.</p>':
                                    '<p id="g_s_goal_owner_new_value" class="o_default_snippet_text">'+str(self.question_frm_id.goal_owner)+'</p>'})
                if self.question_frm_id.analysis_settlement:
                    imgDict.update({'<p id="g_s_analysis_new_value" class="o_default_snippet_text">Duplicate blocks and columns to add more features.</p>':
                                    '<p id="g_s_analysis_new_value" class="o_default_snippet_text">'+str(self.question_frm_id.analysis_settlement)+'</p>'})

                # Snippet Inleiding
                if self.question_frm_id.lead_id and self.question_frm_id.lead_id.user_id:
                    imgDict.update({'<span id="quot_name" class="o_default_snippet_text">Dhr Ferry Nieuwboer':
                                    '<span id="quot_name" class="o_default_snippet_text">'+str(self.question_frm_id.lead_id.user_id.name)})
                if self.question_frm_id.date_opportunity:
                    imgDict.update({'<span id="quote_date" class="o_default_snippet_text">date</span>':
                                    '<span id="quote_date" class="o_default_snippet_text">'+str(self.question_frm_id.date_opportunity)+'</span>'})
                if self.question_frm_id.lead_id:
                    imgDict.update({'<span id="quote_soort" class="o_default_snippet_text">aanbouw/ hoek/ kopgevel/groot deel </span>':
                                    '<span id="quote_soort" class="o_default_snippet_text">'+str(self.question_frm_id.lead_id.soort)+'</span>'})
                if self.question_frm_id.partner_id and self.question_frm_id.partner_id.street:
                    imgDict.update({'<span id="customer_street" class="o_default_snippet_text">street</span>':
                                    '<span id="customer_street" class="o_default_snippet_text">'+str(self.question_frm_id.partner_id.street)+'</span>'})
                if self.question_frm_id.partner_id and self.question_frm_id.partner_id.city:
                    imgDict.update({'<span id="customer_city" class="o_default_snippet_text">Great stories</span>':
                                    '<span id="customer_city" class="o_default_snippet_text">'+str(self.question_frm_id.partner_id.city)+'</span>'})

                # Snippet Opportunity Question Table
                if self.website_description.find('formiler_data_table') != -1:# or self.website_desc_footer.find('formiler_data_table') != -1:
                    my_dict = {}
                    for foundation_construction_id in self.question_frm_id.foundation_construction_ids:
                        if foundation_construction_id.is_selected == True:
                            my_dict.update({'foundation_construction_name': foundation_construction_id.name,
                                            'foundation_construction_image': foundation_construction_id.image})
                    if my_dict:
                        imgDict.update({'<span id="foundation_construction_name_image_id" class="o_default_snippet_text">foundation construction ids</span>':
                                        '<span id="foundation_construction_name_image_id" class="o_default_snippet_text">' + my_dict.get('foundation_construction_name') + '<img src="data:image/jpeg;base64,'+str(my_dict.get('foundation_construction_image'))+'"/> </span>'})
                    if self.question_frm_id.faced_construction:
                        imgDict.update({'<span id="faced_construction_id" class="o_default_snippet_text">Gevelopbouw</span>':
                                        '<span id="faced_construction_id" class="o_default_snippet_text">'+str(self.question_frm_id.faced_construction)+'</span>'})
                    if self.question_frm_id.floor_construction:
                        imgDict.update({'<span id="flore_construction_id" class="o_default_snippet_text">Vloeropbouw bgg</span>':
                                        '<span id="flore_construction_id" class="o_default_snippet_text">'+str(self.question_frm_id.floor_construction)+'</span>'})
                    if self.question_frm_id.floor_construction_verd:
                        imgDict.update({'<span id="floor_construction_verd_id" class="o_default_snippet_text">Vloeropbouw 1* verdieping</span>':
                                        '<span id="floor_construction_verd_id" class="o_default_snippet_text">'+str(self.question_frm_id.floor_construction_verd)+'</span>'})
                    if self.question_frm_id.floor_construction_verd_2:
                        imgDict.update({'<span id="floor_construction_verd_2_id" class="o_default_snippet_text">Vloeropbouw 2* verdieping</span>':
                                        '<span id="floor_construction_verd_2_id" class="o_default_snippet_text">'+str(self.question_frm_id.floor_construction_verd_2)+'</span>'})
                    if self.question_frm_id.leads:
                        imgDict.update({'<span id="lead_id" class="o_default_snippet_text">Leads</span>':
                                        '<span id="lead_id" class="o_default_snippet_text">'+str(self.question_frm_id.leads)+'</span>'})
                    if self.question_frm_id.dakbouw:
                        imgDict.update({'<span id="Dakbouw_id" class="o_default_snippet_text">Dakopbouw</span>':
                                        '<span id="Dakbouw_id" class="o_default_snippet_text">'+str(self.question_frm_id.dakbouw)+'</span>'})
                    if self.question_frm_id.inspection_foundation_depth:
                        imgDict.update({'<span id="inspection_foundation_depth_id" class="o_default_snippet_text">Inspectie Putje</span>':
                                        '<span id="inspection_foundation_depth_id" class="o_default_snippet_text">'+str(self.question_frm_id.inspection_foundation_depth)+'</span>'})
                    if self.question_frm_id.location_pipping_ground:
                        imgDict.update({'<span id="location_pipping_ground_id" class="o_default_snippet_text">Ligging leidingwerk</span>':
                                        '<span id="location_pipping_ground_id" class="o_default_snippet_text">'+str(self.question_frm_id.location_pipping_ground)+'</span>'})
                    if self.question_frm_id.possible_settings:
                        imgDict.update({'<span id="possible_settings_id" class="o_default_snippet_text">Maximale gemeten zetting</span>':
                                        '<span id="possible_settings_id" class="o_default_snippet_text">'+str(self.question_frm_id.possible_settings)+'</span>'})
                    if self.question_frm_id.action_resident:
                        imgDict.update({'<span id="action_resident_id" class="o_default_snippet_text">Actie Bewoner</span>':
                                        '<span id="action_resident_id" class="o_default_snippet_text">'+str(self.question_frm_id.action_resident)+'</span>'})
                    if self.question_frm_id.action_total_wall:
                        imgDict.update({'<span id="action_total_wall_id" class="o_default_snippet_text">Actie DFH</span>':
                                        '<span id="action_total_wall_id" class="o_default_snippet_text">'+str(self.question_frm_id.action_total_wall)+'</span>'})
                    if self.question_frm_id.parkeren:
                        imgDict.update({'<span id="parkeren" class="o_default_snippet_text">Parkeren</span>':
                                        '<span id="parkeren" class="o_default_snippet_text">'+str(self.question_frm_id.parkeren)+'</span>'})
                    if self.question_frm_id.toegang:
                        imgDict.update({'<span id="toegang" class="o_default_snippet_text">Toegang</span>':
                                        '<span id="toegang" class="o_default_snippet_text">'+str(self.question_frm_id.toegang)+'</span>'})
                    if self.question_frm_id.tuin:
                        imgDict.update({'<span id="tuin" class="o_default_snippet_text">Tuin</span>':
                                        '<span id="tuin" class="o_default_snippet_text">'+str(self.question_frm_id.tuin)+'</span>'})
                    if self.question_frm_id.bomen:
                        imgDict.update({'<span id="bomen" class="o_default_snippet_text">Bomen</span>':
                                        '<span id="bomen" class="o_default_snippet_text">'+str(self.question_frm_id.bomen)+'</span>'})
                    if self.question_frm_id.kraan:
                        imgDict.update({'<span id="kraan" class="o_default_snippet_text">Kraan</span>':
                                        '<span id="kraan" class="o_default_snippet_text">'+str(self.question_frm_id.kraan)+'</span>'})
                    if self.question_frm_id.grondwerk:
                        imgDict.update({'<span id="grondwerk" class="o_default_snippet_text">Grondwerk</span>':
                                        '<span id="grondwerk" class="o_default_snippet_text">'+str(self.question_frm_id.grondwerk)+'</span>'})
                    if self.question_frm_id.aanvullend:
                        imgDict.update({'<span id="aanvullend" class="o_default_snippet_text">Aanvullend</span>':
                                        '<span id="aanvullend" class="o_default_snippet_text">'+str(self.question_frm_id.aanvullend)+'</span>'})

            for key, val in imgDict.items():
                description = description.replace(
                    key.encode('utf-8'), val.encode('utf-8'))
                # footer = footer.replace(
                #     key.encode('utf-8'), val.encode('utf-8'))
            self.website_description = description
            # self.website_desc_footer = footer
        return self.website_description


class CrmABC(models.Model):
    """ Partner Model inherit"""

    _inherit = "crm.lead"

    customer_type = fields.Selection(
        selection_add=[('formulier_one', 'Formulier one')])

class QuestionFormulierABC(models.Model):
    """ Question Formulier Model inherit"""

    _inherit = "question.formulier"

    def _default_line_ids(self):
        pr_lines = []
        foundation_img_ids = self.env['foundation.image'].search([])
        for foundation_id in foundation_img_ids:
            pr_lines.append((0, 0, {
                'name': foundation_id.name,
                'image': foundation_id.image,
            }))
        return pr_lines

    house_info = fields.Text('Description of the House', track_visibility='always',
                                default='Het betreft hier een aanbouw van gebouw uit 2000 welke aan linker zijde weg zakt')
    goal_owner = fields.Text('Wish Owner', track_visibility='always',
                                default='De wens van u is het stabiliseren van de fundering en indien mogelijk het liften hiervan')
    analysis_settlement = fields.Text('Our Analysis', track_visibility='always',
                                default='Uit onze prik acties en Waterpasmetingen concluderen wij dat de draagkracht van de grond niet overal het zelfde is en dat het gebouw plaatselijk een grotere zetting heeft. Piekbelastingen door verbouw werkzaamheden. Verkeerstrillingen kunnen de situatie hebben verergerd.')
    faced_construction = fields.Selection([('Spouwmuur', 'Spouwmuur'),
                                ('Steensmuur', 'Steensmuur'),
                                ('Halfsteensmuur met klamp', 'Halfsteensmuur met klamp')], string='Façade Construction',
                                track_visibility='always', default='Spouwmuur')
    gebied = fields.Selection([('Noord', 'Noord'),
                                ('Midden', 'Midden'),
                                ('Zuid', 'Zuid')], string='Area',
                                track_visibility='always')  
    floor_construction = fields.Selection([('zie tekening', 'zie tekening'),
                                ('Beton ; plaat op zand - Vrij tussen muren',
                                 'Beton ; plaat op zand - Vrij tussen muren'),
                                ('Beton ; plaat op zand – verbonden aan muren',
                                 'Beton ; plaat op zand – verbonden aan muren'),
                                ('Hout; vloerbalken oplegging – zijgevel',
                                 'Hout; vloerbalken oplegging – zijgevel'),
                                ('Hout; vloerbalken oplegging – achtergevel',
                                 'Hout; vloerbalken oplegging – achtergevel'),
                                ('Hout; vloerbalken oplegging – zie tekening',
                                 'Hout; vloerbalken oplegging – zie tekening'),
                                ('Broodjes; balken oplegging – zijgevel',
                                 'Broodjes; balken oplegging – zijgevel'),
                                ('Broodjes; balken oplegging – achtergevel',
                                 'Broodjes; balken oplegging – achtergevel'),
                                ('Broodjes; balken oplegging - zie tekening', 'Broodjes; balken oplegging - zie tekening')],
                                string='Floor Construction bgg', track_visibility='always')
    floor_construction_verd = fields.Selection([('zie tekening', 'zie tekening'),
                                ('Niet van toepassing', 'Niet van toepassing'),
                                ('Beton; kanaalplaat oplegging – zijgevel',
                                 'Beton; kanaalplaat oplegging – zijgevel'),
                                ('Beton; kanaalplaat oplegging – achtergevel',
                                 'Beton; kanaalplaat oplegging – achtergevel'),
                                ('Beton; kanaalplaat oplegging - zie tekening',
                                 'Beton; kanaalplaat oplegging - zie tekening'),
                                ('Hout; vloerbalken oplegging – zijgevel',
                                 'Hout; vloerbalken oplegging – zijgevel'),
                                ('Hout; vloerbalken oplegging – achtergevel',
                                 'Hout; vloerbalken oplegging – achtergevel'),
                                ('Hout; vloerbalken oplegging – zie tekening', 'Hout; vloerbalken oplegging – zie tekening')],
                               string='Floor Construction 1* verdieping', track_visibility='always')
    floor_construction_verd_2 = fields.Selection([('zie tekening', 'zie tekening'),
                                ('Niet van toepassing', 'Niet van toepassing'),
                                ('Beton; kanaalplaat oplegging – zijgevel',
                                'Beton; kanaalplaat oplegging – zijgevel'),
                                ('Beton; kanaalplaat oplegging – achtergevel',
                                'Beton; kanaalplaat oplegging – achtergevel'),
                                ('Beton; kanaalplaat oplegging - zie tekening',
                                'Beton; kanaalplaat oplegging - zie tekening'),
                                ('Hout; vloerbalken oplegging – zijgevel',
                                'Hout; vloerbalken oplegging – zijgevel'),
                                ('Hout; vloerbalken oplegging – achtergevel',
                                'Hout; vloerbalken oplegging – achtergevel'),
                                ('Hout; vloerbalken oplegging – zie tekening', 'Hout; vloerbalken oplegging – zie tekening')],
                                string='Floor Construction 2* verdieping', track_visibility='always')
    leads = fields.Selection([('zie tekening', 'zie tekening'),
                                ('Niet van toepassing', 'Niet van toepassing'),
                                ('Beton; kanaalplaat oplegging – zijgevel',
                                 'Beton; kanaalplaat oplegging – zijgevel'),
                                ('Beton; kanaalplaat oplegging – achtergevel',
                                 'Beton; kanaalplaat oplegging – achtergevel'),
                                ('Beton; kanaalplaat oplegging - zie tekening',
                                 'Beton; kanaalplaat oplegging - zie tekening'),
                                ('Hout; vloerbalken oplegging – zijgevel',
                                 'Hout; vloerbalken oplegging – zijgevel'),
                                ('Hout; vloerbalken oplegging – achtergevel',
                                 'Hout; vloerbalken oplegging – achtergevel'),
                                ('Hout; vloerbalken oplegging – zie tekening', 'Hout; vloerbalken oplegging – zie tekening')],
                                string='Leads', track_visibility='always')
    dakbouw = fields.Selection([('Zie tekening', 'Zie tekening'),
                                ('Houten kapcontructie', 'Houten kapcontructie'),
                                ('Platdak Hout','Platdak Hout'),
                                ('Platdak Beton', 'Platdak Beton'),],
                               string='Dakopbouw', track_visibility='always')
    roof_covering = fields.Selection([('dakpan', 'dakpan'),
                                ('bitumen', 'bitumen'),
                                ('glas', 'glas'),
                                ('riet', 'riet')],
                                string='Roof covering', track_visibility='always')
    foundation_construction_ids = fields.One2many('foundation.image.selection', 'question_frm_id',
                                string="Foundation Construction", default=_default_line_ids)
    inspection_foundation_depth = fields.Text('Inspection well Foundation depth Groundwater', track_visibility='always',
                                default='Fundering diepte cm onder Maaiveld \n Geen Grondwater op cm onder Maaiveld')
    location_pipping_ground = fields.Text('Location of piping in the Ground (Info Residents)', track_visibility='always',
                                default='Op cm afstand evenwijdig aan Achtergevel / Langs Gevel')
    possible_settings = fields.Text('Possible cause of Setting', track_visibility='always',
                                default='Weinig Draagkrachtige Grond met prikstok geconstateerd \n Piekbelasting door verbouw werkzaamheden')
    action_resident = fields.Text('Action Resident', track_visibility='always',
                                default='Gaat zelf Tuin opnieuw Aanleggen \n Will zelf Graafwerkzaamheden doen.')
    action_total_wall = fields.Text('Action Total Wall', track_visibility='always',
                                default='Stabiliseren / liften van Uitbouw \n Scheurherstel Buitengevel / binnen, Werkhoogte +/- mtr')
    level_measurement_result = fields.Char('Level Measurement Result on Supplied Construction Plan',
                                track_visibility='always')
    notes_calculation = fields.Text('Notes Engineering / Calculation', track_visibility='always',
                                default='Werkzaamheden met .. man uitvoeren In werk controleren; …(wapening/fund. Afmeting) Palen ongeveer .. cm in dragende zandlaag aanbrengen Let op fundering diepte; niet te diep/laagdikte .. mtr Verwachte draaimoment; 3 kNm')

    aantal_schroefpalen = fields.Integer('Aantal Schroefpalen')
    sondering_diepte = fields.Integer('Depth bearing base layer t.o. reference in meters')
    gkosten_funderingsherstel = fields.Integer('Gkosten Funderingsherstel')
    gkosten_scheurherstel = fields.Integer('Gkosten Scheurherstel')
    schroefpaaldiameter = fields.Selection([('360', '360'),
                                            ('260', '260')], string='Diameter Schroefpalen', track_visibility='always')

    parkeren = fields.Text('Parkeren')
    toegang = fields.Text('Toegang')
    tuin = fields.Text('Tuin')
    bomen = fields.Text('Bomen')
    kraan = fields.Text('Kraan')
    grondwerk = fields.Text('Grondwerk')
    aanvullend = fields.Text('Aanvullend')

    image_1 = fields.Binary('Left view of object',
                            track_visibility='always', attachment=True)
    image_2 = fields.Binary('Front view of object',
                            track_visibility='always', attachment=True)
    image_3 = fields.Binary('Right view of object',
                            track_visibility='always', attachment=True)
    image_4 = fields.Binary('Level Measurement',
                            track_visibility='always', attachment=True)
    image_5 = fields.Binary('Accessibility for Crane',
                            track_visibility='always', attachment=True)
    image_6 = fields.Binary('Excavated Foundation',
                            track_visibility='always', attachment=True)
    image_7 = fields.Binary(
        'Crack in Masonry', track_visibility='always', attachment=True)
    image_8 = fields.Binary('Additional Information',
                            track_visibility='always', attachment=True)

    plattegrond_img = fields.Binary('Map', track_visibility='always', attachment=True)
    fundering_img = fields.Binary('Foundation', track_visibility='always', attachment=True)
    blueprint_img = fields.Binary('Blueprint', track_visibility='always', attachment=True)
    lot_img = fields.Binary('Lot', track_visibility='always', attachment=True)
    extra_drawing_1_img = fields.Binary('Extra Drawing 1', track_visibility='always', attachment=True)
    extra_drawing_2_img = fields.Binary('Extra Drawing 2', track_visibility='always', attachment=True)
    note = fields.Text('Note')

class FoundationImageSelection(models.Model):
    """ Foundation Construction Images"""

    _name = 'foundation.image.selection'
    _description = 'Foundation Construction Images'

    name = fields.Char('Name')
    image = fields.Binary('Image', attachment=True)
    is_selected = fields.Boolean('-')
    question_frm_id = fields.Many2one(
        'question.formulier', 'Related Form', readonly=True)

class FoundationImage(models.Model):
    """ Foundation Images"""

    _name = 'foundation.image'
    _description = 'Foundation Images'

    name = fields.Char('Name')
    image = fields.Binary('Image', attachment=True)
