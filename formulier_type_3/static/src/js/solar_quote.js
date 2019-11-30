odoo.define('formulier_type_3.solar_quote', function (require) {
    "use strict";

    var ajax = require('web.ajax');

    $( document ).ready(function() {

        var clickwatch = (function(){
              var timer = 0;
              return function(callback, ms){
                clearTimeout(timer);
                timer = setTimeout(callback, ms);
              };
        })();

        $('#loading').hide();

        $(function(){
            $("#solar_type").select2();
        });

        if ($("#nav_tabs_solar_form").length) {
            $(this).on('change', "input[name='energy_wat_piek']", function () {
                clickwatch(function() {
                    if ($("#energy_wat_piek").val()) {
                        ajax.jsonRpc("/formulier/quote_infos", 'call', {'energy': parseFloat($("#energy_wat_piek").val())}).then(
                            function(data) {
                                var selectConverter = $("select[name='converter_product']");
                                var child = selectConverter.parent().parent();
                                _.each(child.children(), function(x) {
                                    x.remove();
                                })
                                child.append(selectConverter[0])
                                if (data.converterProducts.length) {
                                    selectConverter.html('');
                                    selectConverter.attr('class','dropdown_image')
                                    _.each(data.converterProducts, function(x) {
                                        var data_image = "/web/image/product.product/"+x[0]+"/image_1920"
                                        var opt = $('<option>').text(x[1])
                                            .attr('value', x[0])
                                            .attr('data-image', data_image)
                                            .attr('data-imagecss', 'flag')
                                            .attr('data-title', x[1]);
                                        selectConverter.append(opt);
                                    });
                                    $("#converter_price")[0].value=data.converterProducts[0][2];
                                }
                                else {
                                    $('.view_converter_product').hide();
                                    selectConverter.html('');
                                    $("#converter_price")[0].value=0;
                                }
                                selectConverter.removeData()
                                selectConverter.msDropdown({roundedBorder:false});
                            }
                        );
                        }
                    });
            });
            $(this).on('change', "input[name='energy_use']", function () {
                clickwatch(function() {
                    if ($("#energy_use").val()) {
                        if ($("#location_correction").val()) {
                            var loc_calculation = $("#energy_use").val() / ($("#location_correction").val()/100);
                            $("input[name='location_calculation']").attr2('value', parseInt(loc_calculation));
                        }
                    }
                }, 500);
            });
            $(this).on('change', "select[name='solar_type']", function () {
                clickwatch(function() {
                    ajax.jsonRpc("/formulier/quote_infos", 'call', {'solar_type': $("#solar_type").val()}).then(
                        function(data) {
                            $('.solar_product')[0].style = 'display: flex;';
                            $('.view_solar_product').hide();
                            $(".panel_price").hide();
                            var solarProduct = $("select[name='solar_product']");
                            var child = solarProduct.parent().parent();
                                _.each(child.children(), function(x) {
                                    x.remove();
                                })
                            child.append(solarProduct[0])
                            if (data.solarP.length) {
                                solarProduct.html('');
                                solarProduct.attr('class','dropdown_image')
                                $(".panel_price")[0].style = 'display: flex;';
                                _.each(data.solarP, function(x) {
                                    var data_image = "/web/image/product.product/"+x[0]+"/image_1920"
                                    var opt = $('<option>').text(x[1]+' '+x[2])
                                        .attr('value', x[0])
                                        .attr('data-image', data_image)
                                        .attr('data-imagecss', 'flag')
                                        .attr('data-title', x[1]+' '+x[2]);
                                    solarProduct.append(opt);
                                });
                                $("#panel_price")[0].value=data.solarP[0][3];
                            }
                            else {
                                solarProduct.html('');
                                $("#panel_price")[0].value=0;
                            }
                            solarProduct.removeData()
                            solarProduct.msDropdown({roundedBorder:false});
                    })
                });
            });
            $(this).on('change', "select[name='pf_select_roof']", function () {
                clickwatch(function() {
                    if ($("#pf_select_roof").val()) {
                        ajax.jsonRpc("/formulier/quote_infos", 'call', {'roof': $("#pf_select_roof").val()}).then(
                            function(data) {
                                var flat_roof = $("select[name='flat_roof_product']");
                                var slanted_roof = $("select[name='slanted_roof_product']");
                                var child = flat_roof.parent().parent();
                                _.each(child.children(), function(x) {
                                    x.remove();
                                })
                                child.append(flat_roof[0])
                                var child = slanted_roof.parent().parent();
                                _.each(child.children(), function(x) {
                                    x.remove();
                                })
                                child.append(slanted_roof[0])
                                if (data.FlatRoofProducts.length) {
                                    flat_roof.html('');
                                    flat_roof.attr('class','dropdown_image')
                                    $(".flat_product")[0].style = 'display: flex;';
                                    _.each(data.FlatRoofProducts, function(x) {
                                        var data_image = "/web/image/product.product/"+x[0]+"/image_1920"
                                        var opt = $('<option>').text(x[1])
                                            .attr('value', x[0])
                                            .attr('data-image', data_image)
                                            .attr('data-imagecss', 'flag')
                                            .attr('data-title', x[1]);
                                        flat_roof.append(opt);
                                    });
                                }
                                else {
                                    flat_roof.html('');
                                    $(".flat_product").hide();
                                    $(".view_flat_roof_product").hide();
                                }
                                if (data.SlantedRoofProducts.length) {
                                    slanted_roof.html('');
                                    slanted_roof.attr('class','dropdown_image')
                                    $(".slanted_product")[0].style = 'display: flex;';
                                    _.each(data.SlantedRoofProducts, function(x) {
                                        var data_image = "/web/image/product.product/"+x[0]+"/image_1920"
                                        var opt = $('<option>').text(x[1])
                                            .attr('value', x[0])
                                            .attr('data-image', data_image)
                                            .attr('data-imagecss', 'flag')
                                            .attr('data-title', x[1]);
                                        slanted_roof.append(opt);
                                    });
                                }
                                else {
                                    slanted_roof.html('');
                                    $(".slanted_product").hide();
                                    $(".view_slanted_roof_product").hide();
                                }
                            flat_roof.removeData()
                            flat_roof.msDropdown({roundedBorder:false});
                            slanted_roof.removeData()
                            slanted_roof.msDropdown({roundedBorder:false});
                            
                            });
                    }
                    else{
                        $(".flat_product").hide()
                        $(".slanted_product").hide();
                        $(".view_flat_roof_product").hide();
                        $(".view_slanted_roof_product").hide();
                    }
                }, 500);
            });

            // call on page load
            $("select[name='pf_select_roof']").change();

            function installation_time() {
                var solar_qty = parseInt($('.solar_qty').text());
                var installation_time = $("select[name='installation_time']")[0];
                var record = $(this);
                record.hours = '';
                if (solar_qty <= 20){
                    record.hours = '16 Hours';
                }
                if (solar_qty >= 20 && solar_qty <= 30){
                    record.hours = '24 Hours';
                }
                if (solar_qty >= 30 && solar_qty <= 40){
                    record.hours = '32 Hours';
                }
                if (record.hours){
                    _.each(installation_time.options, function(op) {
                        if (op.getAttribute('value') == record.hours){
                            var option_index = op.index;
                            installation_time.selectedIndex = option_index;
                        }
                    });
                }
            }
            $(this).on('change click', "select[name='solar_product']", function () {
                clickwatch(function() {
                    if ($("#solar_product").val()){
                        ajax.jsonRpc("/formulier/quote_infos", 'call', {
                            'product_id': parseInt($("#solar_product").val())
                        }).then(
                            function(data) {
                                $("input[name='solar_watt_piek']").attr2('value', data.energy_wat_piek);
                                if (data.solarProduct.length) {
                                    $(".view_solar_product").show();
                                    // $("#panel_price").show();
                                    var src = "/web/image/product.product/"+data.solarProduct[0][0]+"/image_1920"
                                    $("img[name='solar_product_image']").attr('src', src);
                                    $("#solar_name").text(data.solarProduct[0][1]);
                                    $('.panel_price')[0].style = 'display: flex;';
                                    $('#panel_price')[0].value = data.solarProduct[0][2]
                                }
                                var watt = $("input[name='solar_watt_piek']").val();
                                var loc_cal = $("input[name='location_calculation']").val();
                                if (watt && loc_cal) {
                                    var sQty = loc_cal / watt;
                                    if (!isNaN(sQty) && isFinite(sQty)) {
                                        $(".s_qty").text(parseInt(sQty) + 1);
                                    }
                                    else {
                                        $(".s_qty").text(1);
                                    }
                                }
                                else {
                                    $(".s_qty").text(1);
                                }
                                var calculation = $(".solar_qty").text() * data.energy_wat_piek;
                                var energy_wat_piek = $("input[name='energy_wat_piek']");
                                energy_wat_piek.attr2('value', calculation);
                                energy_wat_piek.change();
                                installation_time();
                            }
                        );
                    }
                }, 500);
            });

            $(this).on('change', "input[name='location_correction']", function (e) {
                clickwatch(function() {
                    if (e.currentTarget.value != parseInt(e.currentTarget.value)){
                        e.currentTarget.value = 0 ;
                        alert('Please enter valid number');
                    }
                    var loc_cor = $("#location_correction").val();
                    if (loc_cor && $("#energy_use").val()) {
                        var loc_calculation = $("#energy_use").val() / (loc_cor/100);
                        $("input[name='location_calculation']").attr2('value', parseInt(loc_calculation));
                    }
                    var watt = $("input[name='solar_watt_piek']").val();
                    var loc_cal = $("input[name='location_calculation']").val();
                    if (watt && loc_cal) {
                        var sQty = loc_cal / watt;
                        if (!isNaN(sQty)) {
                            $(".s_qty").text(parseInt(sQty) + 1);
                        }
                        else {
                            $(".s_qty").text(sQty);
                        }
                    }
                    else {
                        $(".s_qty").text(1);
                    }
                    var calculation = parseInt($(".solar_qty").text()) * $("input[name='solar_watt_piek']").val();
                    var energy_wat_piek = $("input[name='energy_wat_piek']");
                    energy_wat_piek.attr2('value', calculation);
                    energy_wat_piek.change()
                    if ($("#optimiser_product").val()) {
                        $(".o_qty").text(parseInt($(".solar_qty").text()));
                    }
                }, 500);
            });
            $("a.update_solar_qty").on('click',function(e) {
                var solar_qty = parseInt($('.solar_qty').text());
                if (e.currentTarget.className.match('add_solar_qty')){
                    var parent_ele = e.currentTarget.parentElement.parentElement;
                    var old_val = parent_ele.getElementsByClassName('solar_qty');
                    old_val[0].innerText = parseInt(old_val[0].innerText) + 1;
                    var calculation = solar_qty * $("input[name='solar_watt_piek']").val();
                    var energy_wat_piek = $("input[name='energy_wat_piek']")
                    energy_wat_piek.attr2('value', calculation);
                    energy_wat_piek.change();
                    if ($("#optimiser_product").val()) {
                        $(".o_qty").text(solar_qty);
                    }
                }
                else{
                    var parent_ele = e.currentTarget.parentElement.parentElement;
                    var old_val = parent_ele.getElementsByClassName('solar_qty');
                    if (parseInt(old_val[0].innerText) > 0){
                        old_val[0].innerText = parseInt(old_val[0].innerText) - 1;
                        var calculation = solar_qty * $("input[name='solar_watt_piek']").val();
                        var energy_wat_piek = $("input[name='energy_wat_piek']")
                        energy_wat_piek.attr2('value', calculation);
                        energy_wat_piek.change();
                        if ($("#optimiser_product").val()) {
                            $(".o_qty").text(solar_qty);
                        }
                    }
                }
                installation_time();
            });
            $(this).on('change click', "select[name='need_converter']", function () {
                if ($("select[name='need_converter']").val() == 'ja'){
                    $(".converter_field")[0].style = 'display: flex;';
                    $(".converter_price")[0].style = 'display: flex;';
                }
                else {
                    $(".converter_field").hide();
                    $(".converter_price").hide();
                    $(".view_converter_product").hide();
                }
            });
            $(this).on('change click', "select[name='converter_product']", function () {
                clickwatch(function() {
                    if ($("#converter_product").val()){
                        ajax.jsonRpc("/formulier/quote_infos", 'call', {
                            'product_id': parseInt($("#converter_product").val())
                        }).then(
                            function(data) {
                                if (data.solarProduct.length) {
                                    $(".view_converter_product").show();
                                    var src = "/web/image/product.product/"+data.solarProduct[0][0]+"/image_1920"
                                    $("img[name='converter_product_image']").attr('src', src);
                                    $("#converter_name").text(data.solarProduct[0][1]);
                                    $(".converter_price")[0].style = 'display: flex;';
                                    $('#converter_price')[0].value=data.solarProduct[0][2];
                                }
                                var optimiser_roof = $("select[name='optimiser_product']");
                                var child = optimiser_roof.parent().parent();
                                _.each(child.children(), function(x) {
                                    x.remove();
                                })
                                child.append(optimiser_roof[0])
                                if (data.optimiserProducts.length) {
                                    optimiser_roof.html('');
                                    optimiser_roof.attr('class','dropdown_image')
                                    _.each(data.optimiserProducts, function(x) {
                                        var data_image = "/web/image/product.product/"+x[0]+"/image_1920"
                                        var opt = $('<option>').text(x[1])
                                            .attr('value', x[0])
                                            .attr('data-image', data_image)
                                            .attr('data-imagecss', 'flag')
                                            .attr('data-title', x[1]);
                                        optimiser_roof.append(opt);
                                    });
                                    $(".optimisers_price")[0].style = 'display: flex;';;
                                    $("#optimisers_price")[0].value = data.optimiserProducts[0][2];
                                }
                                else {
                                    optimiser_roof.html('');
                                    $(".view_optimiser_product").hide();
                                    $(".optimisers_price").hide()
                                }
                                optimiser_roof.removeData()
                                optimiser_roof.msDropdown({roundedBorder:false});
                            }
                        );
                    }
                }, 500);
            });
            $("a.update_converter_qty").on('click',function(e) {
                if (e.currentTarget.className.match('add_converter_qty')){
                    var parent_ele = e.currentTarget.parentElement.parentElement;
                    var old_val = parent_ele.getElementsByClassName('converter_qty');
                    old_val[0].innerText = parseInt(old_val[0].innerText) + 1;
                }
                else{
                    var parent_ele = e.currentTarget.parentElement.parentElement;
                    var old_val = parent_ele.getElementsByClassName('converter_qty');
                    if (parseInt(old_val[0].innerText) > 0){
                        old_val[0].innerText = parseInt(old_val[0].innerText) - 1;
                    }
                }
            });
            $(this).on('change click', "select[name='flat_roof_product']", function () {
                clickwatch(function() {
                    if ($("#flat_roof_product").val()){
                        ajax.jsonRpc("/formulier/quote_infos", 'call', {
                            'product_id': parseInt($("#flat_roof_product").val())
                        }).then(
                            function(data) {
                                if (data.solarProduct.length) {
                                    $(".view_flat_roof_product").show();
                                    var src = "/web/image/product.product/"+data.solarProduct[0][0]+"/image_1920"
                                    $("img[name='flat_roof_product_image']").attr('src', src);
                                    $("#flat_roof_name").text(data.solarProduct[0][1]);
                                    var opt_qty = $('.optimiser_qty');
                                    var roof_qty = $(".flat_roof_qty");
                                    var flat_qty = $(".actual_flat_roof_qty");
                                    if (opt_qty.length && roof_qty.length){
                                        roof_qty[0].innerText = parseInt(opt_qty[0].innerText)
                                        flat_qty[0].innerText = parseInt(opt_qty[0].innerText)
                                    }
                                }
                            }
                        );
                    }
                }, 500);
            });
            $(this).on('change click', "select[name='slanted_roof_product']", function () {
                clickwatch(function() {
                    if ($("#slanted_roof_product").val()){
                        ajax.jsonRpc("/formulier/quote_infos", 'call', {
                            'product_id': parseInt($("#slanted_roof_product").val())
                        }).then(
                            function(data) {
                                if (data.solarProduct.length) {
                                    $(".view_slanted_roof_product").show();
                                    var src = "/web/image/product.product/"+data.solarProduct[0][0]+"/image_1920"
                                    $("img[name='slanted_roof_product_image']").attr('src', src);
                                    $("#slanted_roof_name").text(data.solarProduct[0][1]);
                                    var opt_qty = $('.optimiser_qty');
                                    var roof_qty = $(".slanted_roof_qty");
                                    var slanted_roof = $(".actual_slanted_roof_qty");
                                    if (opt_qty.length && roof_qty.length){
                                        roof_qty[0].innerText = parseInt(opt_qty[0].innerText)
                                        slanted_roof[0].innerText = parseInt(opt_qty[0].innerText)
                                    }
                                }
                            }
                        );
                    }
                }, 500);
            });
            $("a.update_roof_qty").on('click',function(e) {
                if (e.currentTarget.className.match('add_roof_qty')){
                    var parent_ele = e.currentTarget.parentElement.parentElement;
                    var old_val = parent_ele.getElementsByClassName('roof_qty');
                    old_val[0].innerText = parseInt(old_val[0].innerText) + 1;
                }
                else{
                    var parent_ele = e.currentTarget.parentElement.parentElement;
                    var old_val = parent_ele.getElementsByClassName('roof_qty');
                    if (parseInt(old_val[0].innerText) > 0){
                        old_val[0].innerText = parseInt(old_val[0].innerText) - 1;
                    }
                }
            });
            $(this).on('change click', "select[name='need_optimiser']", function () {
                if ($("select[name='need_optimiser']").val() == 'ja'){
                    $(".optimiser_field")[0].style = 'display: flex;';
                    $(".optimisers_price")[0].style = 'display: flex;';
                }
                else {
                    $(".optimiser_field").hide();
                    $(".view_optimiser_product").hide();
                    $(".optimisers_price").hide();
                }
            });
            $(this).on('change click', "select[name='optimiser_product']", function () {
                clickwatch(function() {
                    if ($("#optimiser_product").val()){
                        ajax.jsonRpc("/formulier/quote_infos", 'call', {
                            'product_id': parseInt($("#optimiser_product").val())
                        }).then(
                            function(data) {
                                if (data.solarProduct.length) {
                                    $(".view_optimiser_product").show();
                                    $(".optimisers_price")[0].style = 'display: flex;';
                                    var src = "/web/image/product.product/"+data.solarProduct[0][0]+"/image_1920"
                                    $("img[name='optimiser_product_image']").attr('src', src);
                                    $("#optimiser_name").text(data.solarProduct[0][1]);
                                    $(".optimisers_price")[0].style = 'display: flex;';
                                    $('#optimisers_price').value = data.solarProduct[0][2]
                                    $(".o_qty").text(parseInt($(".solar_qty").text()));
                                }
                            }
                        );
                    }
                }, 500);
            });
            $("a.update_optimiser_qty").on('click',function(e) {
                if (e.currentTarget.className.match('add_optimiser_qty')){
                    var parent_ele = e.currentTarget.parentElement.parentElement;
                    var old_val = parent_ele.getElementsByClassName('optimiser_qty');
                    old_val[0].innerText = parseInt(old_val[0].innerText) + 1;
                }
                else{
                    var parent_ele = e.currentTarget.parentElement.parentElement;
                    var old_val = parent_ele.getElementsByClassName('optimiser_qty');
                    if (parseInt(old_val[0].innerText) > 0){
                        old_val[0].innerText = parseInt(old_val[0].innerText) - 1;
                    }
                }
            });
            $(this).on('change click', "select[name='need_discount']", function () {
                if ($("select[name='need_discount']").val() == 'ja'){
                    $(".discount_field")[0].style = 'display: flex;';
                    $(".discount_qty")[0].style = 'display: flex;';
                }
                else {
                    $(".discount_field").hide();
                    $(".discount_qty").hide();
                    $(".view_discount_product").hide();
                }
            });
            $(this).on('change click', "select[name='discount_product']", function () {
                clickwatch(function() {
                    if ($("#discount_product").val()){
                        ajax.jsonRpc("/formulier/quote_infos", 'call', {
                            'product_id': parseInt($("#discount_product").val())
                        }).then(
                            function(data) {
                                if (data.solarProduct.length) {
                                    $(".view_discount_product").show();
                                    var src = "/web/image/product.product/"+data.solarProduct[0][0]+"/image_1920"
                                    $("img[name='discount_product_image']").attr('src', src);
                                    $("#discount_name").text(data.solarProduct[0][1]);
                                }
                            }
                        );
                    }
                }, 500);
            });
            $(this).on('change click', "select[name='need_discount_2']", function () {
                if ($("select[name='need_discount_2']").val() == 'ja'){
                    $(".amount_range")[0].style = 'display: flex;';
                }
                else {
                    $(".amount_range").hide();
                }
            });
            $(this).on('change', "input[name='amount_range']", function (e) {
                clickwatch(function() {
                    if (e.currentTarget.value != parseInt(e.currentTarget.value)){
                        e.currentTarget.value = 0 ;
                        alert('Please enter valid number');
                    }
                });
            });
            $(this).on('change click', "select[name='stekkers_product']", function () {
                clickwatch(function() {
                    if ($("#stekkers_product").val()){
                        ajax.jsonRpc("/formulier/quote_infos", 'call', {
                            'product_id': parseInt($("#stekkers_product").val())
                        }).then(
                            function(data) {
                                if (data.solarProduct.length) {
                                    $(".view_stekkers_product").show();
                                    var src = "/web/image/product.product/"+data.solarProduct[0][0]+"/image_1920"
                                    $("img[name='stekkers_product_image']").attr('src', src);
                                    $("#stekkers_name").text(data.solarProduct[0][1]);
                                }
                            }
                        );
                    }
                }, 500);
            });
            $(this).on('change click', "select[name='remain_material']", function () {
                clickwatch(function() {
                    if ($("#remain_material").val()){
                        ajax.jsonRpc("/formulier/quote_infos", 'call', {
                            'product_id': parseInt($("#remain_material").val())
                        }).then(
                            function(data) {
                                if (data.solarProduct.length) {
                                    $(".view_material_product").show();
                                    var src = "/web/image/product.product/"+data.solarProduct[0][0]+"/image_1920"
                                    $("img[name='material_product_image']").attr('src', src);
                                    $("#material_name").text(data.solarProduct[0][1]);
                                }
                            }
                        );
                    }
                }, 500);
            });
            $(this).on('change click', "select[name='vat_refund_product']", function () {
                clickwatch(function() {
                    if ($("#vat_refund_product").val()){
                        ajax.jsonRpc("/formulier/quote_infos", 'call', {
                            'product_id': parseInt($("#vat_refund_product").val())
                        }).then(
                            function(data) {
                                if (data.solarProduct.length) {
                                    $(".view_vat_product").show();
                                    var src = "/web/image/product.product/"+data.solarProduct[0][0]+"/image_1920"
                                    $("img[name='vat_product_image']").attr('src', src);
                                    $("#vat_name").text(data.solarProduct[0][1]);
                                }
                            }
                        );
                    }
                }, 500);
            });
            $(this).on('click', ".o_website_create_quote, .o_website_eval_quote", function (e) {
                var allData = {
                    'solar_id': parseInt($("#solar_product").val()),
                    'solar_qty': parseInt($('.solar_qty').text()),
                    'location_correction': parseInt($('#location_correction').val()),
                    'is_converter': $("select[name='need_converter']").val(),
                    'converter_id': parseInt($("#converter_product").val()),
                    'converter_qty': parseInt($('.converter_qty').text()),
                    'converter_price': parseInt($('#converter_price').val()),
                    'panel_price': parseInt($('#panel_price').val()),
                    'optimisers_price' : parseInt($('#optimisers_price').val()),
                    'roof': $("select[name='pf_select_roof']").val(),
                    'flat_roof_id': parseInt($("#flat_roof_product").val()),
                    'flat_roof_qty': parseInt($('.flat_roof_qty').text()),
                    'slanted_roof_id': parseInt($("#slanted_roof_product").val()),
                    'slanted_roof_qty': parseInt($('.slanted_roof_qty').text()),
                    'stekkers_id': parseInt($("#stekkers_product").val()),
                    'installation_time': $("select[name='installation_time']").val(),
                    'material_id': parseInt($("#remain_material").val()),
                    'vat_id': parseInt($("#vat_refund_product").val()),
                    'is_optimizer': $("select[name='need_optimiser']").val(),
                    'optimiser_id': parseInt($("#optimiser_product").val()),
                    'optimiser_qty': parseInt($('.optimiser_qty').text()),
                    'is_discount': $("select[name='need_discount']").val(),
                    'discount_id': parseInt($("#discount_product").val()),
                    'discount_qty': parseInt($("input[name='discount_qty']").val()),
                    'is_discount_2': $("select[name='need_discount_2']").val(),
                    'amount_range': $("input[name='amount_range']").val(),
                    'template_id': parseInt($("select[name='quote_template_id']").val()),
                }
                var que_id = e.target.getAttribute('value');
                $('#loading').show();
                if (e.target.className.search('o_website_eval_quote') != -1){
                    ajax.jsonRpc("/formulier/quote_create", 'call', {
                                    'quoteData': allData,
                                    'que_id': que_id,
                                    'eval_quote':true,
                        }).then(
                            function(data) {
                                $('#loading').hide();
                                var quote_button = $('#quote_create');
                                if (data.length > 1){
                                    quote_button.before('<div class="row"><div class="col-lg-7 col-md-7 col-lg-offset-2"><div class="col-lg-6"><strong>Score:</strong><span> '+String(data[0])+'</span></div><div class="col-lg-6"><strong>Totaal excl btw:</strong><span> '+String(data[1])+'</span></div></div></div>')
                                }
                                if (data.length < 2){
                                    quote_button.before('<div class="row"><div class="col-lg-7 col-md-7 col-lg-offset-2"><div class="col-lg-6"><strong>Totaal excl btw:</strong><span> '+String(data[0])+'</span></div></div></div>')
                                }
                            }
                        );
                }
                else{
                    ajax.jsonRpc("/formulier/quote_create", 'call', {
                                'quoteData': allData,
                                'que_id': que_id,
                                'eval_quote':false,
                    }).then(
                        function(data) {
                            $('#loading').hide();
                            window.open(data.url, '_blank');
                            $('.o_website_form_send').click();
                        }
                    );
                }
            });
        }
        $("select[name='is_earthing_total_length']").on('click', function(e){
            if (e.currentTarget.value == 'ja'){
                console.log("....clicked");
                $('.is_earthing_total_length')[0].style = 'display: flex;';
            }
            else{
                $('.is_earthing_total_length')[0].style = 'display:none;';
            }
        });
        $("select[name='is_utp_total_length']").on('click', function(e){
            if (e.currentTarget.value == 'ja'){
                console.log("....clicked");
                $('.is_utp_total_length')[0].style = 'display: flex;';
            }
            else{
                $('.is_utp_total_length')[0].style = 'display:none;';
            }
        });
    });

});