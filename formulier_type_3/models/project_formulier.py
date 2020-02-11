    # -*- coding: utf-8 -*-

import datetime
from odoo import api, fields, models, _
import re

class CrmThree(models.Model):
    """ Partner Model inherit"""

    _inherit = "crm.lead"

    customer_type = fields.Selection(
        selection_add=[('formulier_three', 'Intake PV')])

class QuestionFormulierThree(models.Model):
    """ Question Formulier Model inherit"""

    _inherit = "question.formulier"

    # @api.depends('solar_product', 'energy_use')
    @api.depends('location_calculation', 'solar_watt_piek', 'solar_product')
    def computeEnergyWatPiek(self):
        for rec in self:
            # if rec.energy_use and rec.solar_product.ec_watt_piek:
            #     rec.energy_wat_piek = rec.energy_use / rec.solar_product.ec_watt_piek
            if rec.location_calculation > 0 and rec.solar_watt_piek:
                cal = rec.location_calculation / rec.solar_watt_piek
                solar_qty = 1
                if (isinstance(cal, float)):
                    solar_qty = int(cal) + 1
                else:
                    solar_qty = cal
                rec.energy_wat_piek = rec.solar_watt_piek * solar_qty

    @api.depends('location_correction', 'energy_use')
    def computeLocation(self):
        for rec in self:
            if rec.location_correction and rec.energy_use:
                rec.location_calculation = rec.energy_use / rec.location_correction

    @api.depends('solar_product')
    def getEnergyWatPiek(self):
        for rec in self:
            rec.solar_watt_piek = rec.solar_product.ec_watt_piek

    # Ontwerpvragen -> Design questions
    roof_surface = fields.Selection([('1', '1'),
                                    ('2', '2'),
                                    ('3', '3'),
                                    ('4', '4'),
                                    ('meer dan 4', 'meer dan 4'),],
                                    string='How many roof surfaces',
                                    default='1',
                                    track_visibility='always')

    # Woning -> Home
    is_permit_required = fields.Selection([('ja', 'ja'),
                                    ('nee', 'nee'),],
                                    string='Is a permit required',
                                    default='nee', track_visibility='always')
    construction_year = fields.Integer(string='Year of construction of the house',
                                    track_visibility='always')
    any_roof_problem = fields.Selection([('ja', 'ja'),
                                    ('nee', 'nee'),],
                                    string='Have you ever had any leaks or other problems with your roof?',
                                    default='nee', track_visibility='always')
    is_buy_rent_property = fields.Selection([('koop', 'koop'),
                                    ('huur', 'huur'),],
                                    string='Is it a rent or buy property?',
                                    default='koop',
                                    track_visibility='always')

    # Aansluiten omvormer -> Connecting the inverter
    string_1 = fields.Integer(string='String 1 (Note: always 6 panels or more in 1 string)',
                            track_visibility='always')
    string_2 = fields.Integer(string='String 2 (Note: always 6 panels or more in 1 string)',
                            track_visibility='always')

    # Bereikbaarheid van de woning en het dak -> Accessibility of the home and the roof
    is_free_space_scaffolding = fields.Selection([('ja', 'ja'),
                                    ('nee', 'nee'),],
                                    string='Is there a free space for scaffolding?',
                                    track_visibility='always')
    is_provision_required = fields.Selection([('ja', 'ja'),
                                    ('nee', 'nee'),],
                                    string='Is a special provision required (telehandler / lift / aerial platform)',
                                    default='nee', track_visibility='always')
    condition_scaffolding_place = fields.Selection([('Gras', 'Gras'),
                                    ('Tuin', 'Tuin'),
                                    ('Zand', 'Zand'),
                                    ('Straat', 'Straat'),
                                    ('Geen steiger te plaatsen', 'Geen steiger te plaatsen'),
                                    ('Geen steiger nodig', 'Geen steiger nodig'),],
                                    string='What is the condition of the surface on which the scaffolding is placed?',
                                    track_visibility='always',
                                    default='Tuin')
    accessibility_rear = fields.Selection([('Brandgang', 'Brandgang'),
                                    ('Door de garage', 'Door de garage'),
                                    ('Vrije rondgang', 'Vrije rondgang'),
                                    ('Door de woning', 'Door de woning'),
                                    ('N.V.T.', 'N.V.T.'),],
                                    string='What is the accessibility of the rear',
                                    track_visibility='always',
                                    default='N.V.T.')
    use_public_road = fields.Selection([('ja', 'ja'),
                                    ('nee', 'nee'),],
                                    string='Use must be made of the public road for the erection of scaffolding or facilities',
                                    default='nee', track_visibility='always')
    access_roof_neighbors = fields.Selection([('Nee', 'Nee'),
                                    ('Ja er is toestemming', 'Ja er is toestemming'),
                                    ('Ja maar er is nog geen toestemming', 'Ja maar er is nog geen toestemming'),],
                                    string='Access to the roof / territory of the neighbors is required',
                                    track_visibility='always')
    distance_bus_to_roof = fields.Selection([('0-10', '0-10'),
                                    ('10-25', '10-25'),
                                    ('25-50', '25-50'),
                                    ('50-100', '50-100'),
                                    ('100-250', '100-250'),
                                    ('250-500', '250-500'),
                                    ('500+', '500+'),],
                                    string='Walking distance from bus to roof access',
                                    track_visibility='always')
    direct_installation_scaffolding = fields.Selection([('ja', 'ja'),
                                    ('nee', 'nee'),
                                    ('Ja, zie foto/video', 'Ja, zie foto/video'),
                                    ('Ja, klant zorgt voor oplossing', 'Ja, klant zorgt voor oplossing'),],
                                    string='Is there an extension / obstacle present that hinders the direct installation of scaffolding or roof lift?',
                                    default='nee', track_visibility='always')

    # Dak -> Roof
    dak_type_of_roof = fields.Selection([('Schuin', 'Schuin'),
                                    ('Plat', 'Plat'),
                                    ('Schuin / Dak', 'Schuin / Dak'),
                                    ('Zadeldak', 'Zadeldak'),],
                                    string='What type (s) of roof is it?',
                                    track_visibility='always')
    condition_of_roof = fields.Selection([('goed', 'goed'),
                                    ('matig', 'matig'),
                                    ('slecht', 'slecht'),
                                    ('onbekend', 'onbekend'),],
                                    string='What is the condition of the roof?',
                                    default='goed',
                                    track_visibility='always')
    asbestos_incorporated_roof = fields.Selection([('ja', 'ja'),
                                    ('nee', 'nee'),
                                    ('ja klant op de hoogte van de gevogen','ja klant op de hoogte van de gevogen'),
                                    ('ja klant niet op de hoogte van de gevogen','ja klant niet op de hoogte van de gevogen')],
                                    string='Is asbestos incorporated in the roof? And is the customer aware of the consequences?',
                                    default='nee', track_visibility='always')
    height_of_gutter = fields.Selection([('0-2.5 m1', '0-2.5 m1'),
                                    ('2.5-4 m1', '2.5-4 m1'),
                                    ('4-6 m1', '4-6 m1'),
                                    ('6-8 m1', '6-8 m1'),
                                    ('8-10 m1', '8-10 m1'),
                                    ('10+', '10+'),],
                                    string='What is the height of the gutter?',
                                    default='8-10 m1',
                                    track_visibility='always')

    # Schuin Dak -> Slanted roof
    slope = fields.Selection([('0-20 graden', '0-20 graden'),
                                    ('20-30 graden', '20-30 graden'),
                                    ('30-40 graden', '30-40 graden'),
                                    ('40-50 graden', '40-50 graden'),
                                    ('50-60 graden', '50-60 graden'),
                                    ('60-70 graden', '60-70 graden'),
                                    ('70+ graden', '70+ graden')],
                                    string='What is the slope?',
                                    track_visibility='always')
    schuin_type_of_roof = fields.Selection([('Pannen', 'Pannen'),
                                    ('Bitumen', 'Bitumen'),
                                    ('Golfplaten', 'Golfplaten'),
                                    ('Staal', 'Staal'),
                                    ('Leien ', 'Leien '),
                                    ('Zink', 'Zink'),
                                    ('Overige', 'Overige'),
                                    ('ASBEST', 'ASBEST'),],
                                    string='What type of roofing is it?',
                                    default='Pannen',
                                    track_visibility='always')
    are_pans_screwed_or_hooked = fields.Selection([('geschroefd', 'geschroefd'),
                                    ('gehaakt', 'gehaakt'),
                                     ('beide', 'beide'),
                                     ('anders', 'anders')],
                                    string='Are the pans screwed or hooked?',
                                    default='geschroefd',
                                    track_visibility='always')

    # Plat Dak -> Flat roof
    gravel_on_roof = fields.Selection([('ja', 'ja'),
                                    ('nee', 'nee'),],
                                    string='Is there gravel on the roof?',
                                    default='nee',
                                    track_visibility='always')
    plat_type_roof = fields.Selection([('Bitumen', 'Bitumen'),
                                    ('EPDM', 'EPDM'),
                                    ('PVC', 'PVC'),
                                    ('Overige', 'Overige'),],
                                    default='Bitumen',
                                    string='What type (s) of roofing is it?',
                                    track_visibility='always')
    roof_terminal_cabling = fields.Selection([('ja', 'ja'),
                                    ('Nee aanleggen ECNL', 'Nee aanleggen ECNL'),
                                    ('nee', 'nee'),
                                    ('Nee klant draagt hier zorg voor', 'Nee klant draagt hier zorg voor'),],
                                    default='nee',
                                    string='Is there a roof terminal for the string cabling',
                                    track_visibility='always')

    # Meterkast -> Fuse box
    main_switch = fields.Selection([('ja', 'ja'),
                                    ('nee', 'nee'),],
                                    string='Is there a main switch?',
                                    default='ja', track_visibility='always')
    is_space_install_earth_leakage = fields.Selection([('ja', 'ja'),
                                    ('nee', 'nee'),],
                                    string='Is there a free space to install the earth leakage circuit breaker?',
                                    default='ja', track_visibility='always')

    # Omvormer -> Inverter
    location_of_inverter = fields.Text(string='Location of the inverter')
    is_space_inverter_cooling = fields.Selection([('ja', 'ja'),
                                    ('nee', 'nee'),],
                                    string='Is there sufficient free space around the inverter for cooling / ventilation purposes?',
                                    default='ja', track_visibility='always')
    is_sturdy_rear_wall = fields.Selection([('ja', 'ja'),
                                    ('nee', 'nee'),],
                                    string='Is a sturdy rear wall available?',
                                    default='ja', track_visibility='always')
    washing_machine_use = fields.Selection([('ja', 'ja'),
                                    ('nee', 'nee'),],
                                    string='Can a washing machine connection be used?',
                                    default='nee', track_visibility='always')

    # Bekabeling -> Cabling
    empty_pipe_use = fields.Selection([('ja', 'ja'),
                                    ('nee', 'nee'),],
                                    default='nee',
                                    string='Can an empty pipe be used?',
                                    track_visibility='always')
    description_inverter = fields.Text(string='Description cable route panels -> inverter')
    description_cable_inverter = fields.Text(string='Description cable inverter -> meter box')
    description_utp_cable = fields.Text(default='NVT',
                                    string='Description UTP cable converter -> meter box')
    want_mount_cable_himself = fields.Selection([('ja', 'ja'),
                                    ('nee', 'nee'),],
                                    string='Does the customer want to mount a cable himself?',
                                    default='nee', track_visibility='always')
    diameter_of_cable = fields.Selection([('3*2.5mm2', '3*2.5mm2'),
                                    ('5*2.5mm2', '5*2.5mm2'),
                                    ('3*4mm2', '3*4mm2'),
                                    ('5*4mm2', '5*4mm2'),
                                    ('5*6mm2', '5*6mm2'),
                                    ('5*10mm2', '5*10mm2'),],
                                    string='When using an existing cable what is the diameter of the cable?')
    internet_connection_wired = fields.Selection([('ja', 'ja'),
                                    ('nee', 'nee'),],
                                    string='The internet connection can be wired',
                                    track_visibility='always')

    # Overige -> Others
    is_entrepreneurship = fields.Selection([('ja', 'ja'),
                                    ('nee', 'nee'),],
                                    string='Is there any entrepreneurship?',
                                    default='nee',
                                    track_visibility='always')
    name_on_bill = fields.Selection([('ja', 'ja'),
                                    ('nee', 'nee'),],
                                    string='Does the name (incl. Initials) on the energy bill / contract match the name on the quote?',
                                    default='ja', track_visibility='always')
    vat_exemption_rules = fields.Selection([('ja', 'ja'),
                                    ('nee', 'nee'),],
                                    string='Do you fall under VAT exemption rules?',
                                    default='nee',
                                    track_visibility='always')
    preservation_product = fields.Selection([('Nee', 'Nee'),
                                    ('Ja niet geinteresseerd', 'Ja niet geinteresseerd'),
                                    ('Ja geinteresseerd', 'Ja geinteresseerd'),
                                    ('Ja offerte', 'Ja offerte')],
                                    string='Do you need other preservation products?',
                                    default='Nee',
                                    track_visibility='always')
    agreements_with_client = fields.Text(string='Other special agreements with client')
    note = fields.Text(string='Note', track_visibility='always')

    scaffolding_site = fields.Binary(string='Scaffolding site', track_visibility='always', attachment=True)
    roof_2 = fields.Binary(string='Roof 2', track_visibility='always', attachment=True)
    roof_3 = fields.Binary(string='Roof 3', track_visibility='always', attachment=True)
    meter_cupboard_1 = fields.Binary(string='Meter cupboard 1', track_visibility='always', attachment=True)
    meter_cupboard_2 = fields.Binary(string='Meter cupboard 2', track_visibility='always', attachment=True)
    place_inverter_comes = fields.Binary(string='Place where the inverter comes', track_visibility='always', attachment=True)
    cable_gradient_panels_inverter = fields.Binary(string='Cable gradient panels -> inverter', track_visibility='always', attachment=True)
    cable_converter_converter_meter = fields.Binary(string='Cable converter converter -> meter box', track_visibility='always', attachment=True)
    roof_plan = fields.Binary(string='Something special: Roof plan', track_visibility='always', attachment=True)
    drawing_field_hand = fields.Binary(string='A drawing field where you with your hand', track_visibility='always', attachment=True)
    parking_spot_three = fields.Binary(string='Parking spot', track_visibility='always', attachment=True)
    house_three = fields.Binary(string='House / Property', track_visibility='always', attachment=True)
    access_three = fields.Binary(string='Access', track_visibility='always', attachment=True)
    roof1_three = fields.Binary(string='Roof 1', track_visibility='always', attachment=True)
    obstacles_three = fields.Binary(string='Obstacles', track_visibility='always', attachment=True)

    #Question for Task
    # Algemeen -> General
    system_vendor_name = fields.Char(string='Vendor name of the system', track_visibility='always')
    email_address = fields.Char(string='E-mail address', track_visibility='always')
    commencement_work_date = fields.Date(string='Date of commencement of work', track_visibility='always',
        default=datetime.date.today())
    delivery_date = fields.Date(string='Delivery date', track_visibility='always', default=datetime.date.today())
    mechanic_name_1 = fields.Char(string='Mechanic Name 1', track_visibility='always')
    mechanic_name_2 = fields.Char(string='Mechanic Name 2', track_visibility='always')
    mechanic_name_3 = fields.Char(string='Mechanic Name 3', track_visibility='always')

    # Dakwerk -> Roofing
    any_damage_detected_start = fields.Selection([('ja', 'ja'),
        ('nee', 'nee')], default='ja', track_visibility='always',
        string='Have any damage already been detected at the start of the work?')
    solar_panels_installed = fields.Selection([
        ('ja', 'ja'), ('nee', 'nee')],
        string='Have the solar panels been installed in accordance with the roof plan?',
        default='ja', track_visibility='always')
    extra_solar_panels_installed = fields.Selection([
        ('Yes, enter the amount for other', 'Yes, enter the amount for other'), ('nee', 'nee')],
        string='Have additional solar panels been installed?',
        default='nee', track_visibility='always')
    waterline_installed = fields.Selection([
        ('ja', 'ja'), ('nee', 'nee')],
        string='Have all plugs from the waterline been installed?',
        default='ja', track_visibility='always')
    cables_separated = fields.Selection([
        ('ja', 'ja'), ('nee', 'nee')],
        string='Are the plus and minus cables separated?',
        default='ja', track_visibility='always')
    pans_pushed = fields.Selection([
        ('ja', 'ja'), ('nee', 'nee')],
        string='Have all pans been pushed back?',
        default='ja', track_visibility='always')
    is_representatives_inspection = fields.Selection([
        ('ja', 'ja'), ('nee', 'nee')],
        string='Is the inspection by the representatives correct?',
        default='ja', track_visibility='always')
    is_roof_plan_fit = fields.Selection([
        ('ja', 'ja'), ('nee', 'nee')],
        string='Does the roof plan fit?',
        default='ja', track_visibility='always')
    what_panel_installed = fields.Char(string='What panels have been installed?', track_visibility='always')

    # Elektrisch -> Electric
    cabling_length = fields.Integer(string='Length of the used string cabling?')
    cable_thickness = fields.Selection([
        ('4mm2', '4mm2'), ('6mm2', '6mm2'), ('10mm2', '10mm2')],
        string='Applied cable thickness of string cabling?',
        default='4mm2', track_visibility='always')
    inverter_length = fields.Integer(string='Length of the inverter wiring used -> meter box?')
    inverter_cable_thickness = fields.Selection([
        ('3x2,5mm2', '3x2,5mm2'), ('5x2,5mm2', '5x2,5mm2'), ('3x4mm2', '3x4mm2'),
        ('5x4mm2', '5x4mm2'), ('5x6mm2', '5x6mm2'), ('5x10mm2', '5x10mm2')],
        string='Applied cable thickness of the inverter -> meter box?',
        default='3x2,5mm2', track_visibility='always')
    is_earthing_total_length = fields.Selection([('ja', 'ja'), ('nee', 'nee')],
     string='Has the earthing been checked for correct installation?')
    earthing_total_length = fields.Integer(
        string='What is the earth cable length?')
    is_utp_total_length = fields.Selection([('ja', 'ja'), ('nee', 'nee')], 
        string='Is the UTP cable connected correctly?')
    utp_total_length = fields.Integer(
        string='What is the length of the UTP cable used?')
    measured_voltage = fields.Integer(string='Measured string voltage - Value')
    measured_panels_voltage = fields.Integer(string='Measured String Voltage - Panels')
    measured_optimizers_voltage = fields.Integer(string='Measured string voltage - Number of optimizers')
    internet_via = fields.Selection([
        ('UTP', 'UTP'),
        ('WiFi', 'WiFi'),
        ('Socket boxes', 'Socket boxes'),
        ('Customer arranges itself', 'Customer arranges itself'),
        ('No internet i.o.m. customer agreement', 'No internet i.o.m. customer agreement')],
        string='Internet connection established via?',
        default='UTP', track_visibility='always')
    is_home_installation_ok = fields.Selection([
        ('ja', 'ja'), ('nee', 'nee')],
        string='Is the home installation still OK after installing the earth leakage circuit breaker?',
        track_visibility='always')

    # Overige -> Others
    extra_panels = fields.Integer(string='How many panels have been installed extra?')
    installation_damages = fields.Text(
        string='What damages have been detected or made during the installation process?')
    other_remarks = fields.Text(string='Other remarks')

    # Afsluiting in te vullen door de de klant -> Closure to be completed by the customer
    is_engineers_work_safely = fields.Selection([
        ('ja', 'ja'), ('nee', 'nee')],
        string='Did our engineers work safely with scaffolding or fall protection?',
        default='ja', track_visibility='always')
    is_workplace_clean = fields.Selection([
        ('ja', 'ja'), ('nee', 'nee')],
        string='Has the workplace been left clean?',
        default='ja', track_visibility='always')
    is_sufficient_explanation = fields.Selection([
        ('ja', 'ja'), ('nee', 'nee')],
        string='Have you received sufficient explanation during installation?',
        default='ja', track_visibility='always')
    setting_explanation = fields.Selection([
        ('ja', 'ja'), ('nee', 'nee')],
        string='Did you have an explanation when setting up the monitoring app?',
        track_visibility='always')
    any_comments = fields.Text(string='Do you have any comments for us?')
    use_home_photos = fields.Selection([
        ('ja', 'ja'), ('nee', 'nee')],
        string='Can we use photos of your home as a reference on the internet?',
        track_visibility='always')
    other_interested_customers = fields.Text(
        string='Do you have other customers who are also interested in our services?')
    receive_order = fields.Char(
        string='order you receive a whopping € 100 application premium.')
    other_discussed = fields.Text(string='Other discussed matters')

    # Welke foto's moeten worden genomen -> Which photos must be taken
    cables_together_1 = fields.Binary(
        string='Are the plus and minus cables together 1', track_visibility='always', attachment=True)
    cables_together_2 = fields.Binary(
        string='Are the plus and minus cables together 2', track_visibility='always', attachment=True)
    cables_together_3 = fields.Binary(
        string='Are the plus and minus cables together 3', track_visibility='always', attachment=True)
    pans_pushed_back = fields.Binary(
        string='All pans pushed back', track_visibility='always', attachment=True)
    photo_roof_1 = fields.Binary(
        string='Overview photo roof 1', track_visibility='always', attachment=True)
    photo_roof_2 = fields.Binary(
        string='Overview photo roof 2', track_visibility='always', attachment=True)
    photo_roof_3 = fields.Binary(
        string='Overview photo roof 3', track_visibility='always', attachment=True)
    outlet_inverter_roof = fields.Binary(
        string='Photo roof outlet inverter -> roof', track_visibility='always', attachment=True)
    work_switch = fields.Binary(
        string='Photo opened work switch', track_visibility='always', attachment=True)
    photo_placement_inverter = fields.Binary(
        string='Overview photo placement inverter + work switch', track_visibility='always', attachment=True)
    inverter_in_operation = fields.Binary(
        string='Photo display inverter in operation', track_visibility='always', attachment=True)
    inverter_internet = fields.Binary(
        string='Photo display inverter internet', track_visibility='always', attachment=True)
    cupboard_opened = fields.Binary(
        string='Photo meter cupboard opened with automatic', track_visibility='always', attachment=True)
    cupboard_closed = fields.Binary(
        string='Meter cupboard closed', track_visibility='always', attachment=True)
    inverter_serial_number = fields.Binary(
        string='Photo serial number inverter', track_visibility='always', attachment=True)
    optimizers_serial_number = fields.Binary(
        string='Photo serial numbers optimizers (Readable!)', track_visibility='always', attachment=True)

    #Questions for solar quote
    energy_use = fields.Float(string='How much energy You use ?', track_visibility='always')
    location_correction = fields.Integer(string="Location Correction")
    location_calculation = fields.Float(string='Location Calculations', compute=computeLocation, store=True)
    solar_type = fields.Many2many('solar.type', string="Solar type")
    solar_product = fields.Many2one('product.product', string='Which solar panel You want ?',
        track_visibility='always')
    solar_watt_piek = fields.Float(string='Solar Energy Watt Piek', compute=getEnergyWatPiek, store=True)
    energy_wat_piek = fields.Float(string='Energy Wat Piek Calclulation', compute=computeEnergyWatPiek,
        track_visibility='always', store=True)
    need_converter = fields.Selection([
        ('ja', 'ja'), ('nee', 'nee')],
        string='Do You need Converter ?',
        track_visibility='always')
    converter_product = fields.Many2one('product.product', string='Which converter we need ?',
        track_visibility='always')
    pf_select_roof = fields.Selection([
        ('Flat Roof', 'Flat Roof'),
        ('Slanted Roof', 'Slanted Roof'),
        ('Mix Roof', 'Mix Roof')],
        string='Is it a flat roof or a slanted roof ?')
    flat_roof_product = fields.Many2one('product.product', string='Which Flat roof system You want ?',
        track_visibility='always')
    slanted_roof_product = fields.Many2one('product.product', string='Which Slanted roof system You want ?',
        track_visibility='always')
    installation_time = fields.Selection([
        ('4 Hours', '4 Hours'),
        ('8 Hours', '8 Hours'),
        ('12 Hours', '12 Hours'),
        ('16 Hours', '16 Hours'),
        ('24 Hours', '24 Hours'),
        ('30 Hours', '30 Hours'),
        ('32 Hours', '32 Hours'),
        ('36 Hours', '36 Hours'),
        ('40 Hours', '40 Hours')],
        string='How many time needed for installation ?')
    stekkers_product = fields.Many2one('product.product', string='Which stekkers You want ?',
        track_visibility='always')
    remain_material = fields.Many2one('product.product', string='Which Overige Materialen You want ?',
        track_visibility='always')
    vat_refund_product = fields.Many2one('product.product', string='Which btw teruggave You want ?',
        track_visibility='always')
    need_optimiser = fields.Selection([
        ('ja', 'ja'), ('nee', 'nee')],
        string='Do You need product Optimisers ?',
        track_visibility='always')
    optimiser_product = fields.Many2one('product.product', string='Which optimiser You want ?',
        track_visibility='always')
    need_discount = fields.Selection([
        ('ja', 'ja'), ('nee', 'nee')],
        string='Do You need Discount ?',
        track_visibility='always')
    discount_product = fields.Many2one('product.product', string='Select Discount',
        track_visibility='always')
    discount_qty = fields.Float(string="Discount Quantity", track_visibility='always')
    need_discount_2 = fields.Selection([
        ('ja', 'ja'), ('nee', 'nee')],
        string='Do You need Discount 2 ?',
        track_visibility='always')
    amount_range = fields.Integer(string='Extra marge')
    quote_template_id = fields.Many2one('sale.order.template', string='Choose your quote template', track_visibility='always')

    converter_price = fields.Float(string="Converter Price")
    panel_price = fields.Float(string="Panel Price")
    optimisers_price = fields.Float(string="Optimisers Price")

    def online_pf_dictionary(self):
        """ online pf possible values"""

        values = super(QuestionFormulierThree, self).online_pf_dictionary()
        if self.customer_type == 'formulier_three':
            productObj = self.env['product.product'].sudo()
            user = self.env.user
            SolarType = self.env['solar.type'].sudo().search([])
            solarProducts = productObj.search([
                ('product_type', '=', 'Solar Panel'),
                ('solar_type','in',self.solar_type.ids)], order='priority')
            converterProducts = productObj.search([
                '&', ('min_product_range', '<=', self.energy_wat_piek),
                ('max_product_range', '>=', self.energy_wat_piek),
                ('product_type', '=', 'Converter')], order='priority')
            FlatRoofProducts = productObj.search([
                ('product_type', '=', 'Flat Roof')], order='priority')
            SlantedRoofProducts = productObj.search([
                ('product_type', '=', 'Slanted Roof')], order='priority')
            optimiserProducts = self.optimiser_product
            stekkerProducts = productObj.search([
                ('product_type', '=', 'Stekkers')], order='priority')
            DiscountProducts = productObj.search([
                ('product_type', '=', 'Discount')], order='priority')
            RemainMaterials = productObj.search([
                ('product_type', '=', 'Overige Materialen')], order='priority')
            vatRefundProducts = productObj.search([
                ('product_type', '=', 'BTW teruggave')], order='priority')
            if not user.template_id:
                QuoteTemplate = self.env['sale.order.template'].sudo().search([])
            else:
                QuoteTemplate = user.template_id
            values.update({'SolarType': SolarType,
                            'solarProducts': solarProducts,
                            'converterProducts': converterProducts,
                            'FlatRoofProducts': FlatRoofProducts,
                            'SlantedRoofProducts': SlantedRoofProducts,
                            'optimiserProducts': optimiserProducts,
                            'stekkerProducts': stekkerProducts,
                            'DiscountProducts': DiscountProducts,
                            'RemainMaterials': RemainMaterials,
                            'vatRefundProducts': vatRefundProducts,
                            'QuoteTemplate': QuoteTemplate,
                            })
        return values

