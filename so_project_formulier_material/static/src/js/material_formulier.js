odoo.define('so_project_formulier_material.material_formulier', function (require) {
'use strict';

    var core = require('web.core');
    var Dialog = require('web.Dialog');
    var Widget = require('web.Widget');
    var rpc = require('web.rpc');
    var QWeb = core.qweb;

    $(document).ready(function () {

        // change signature canvas default width
        $('#nav_tabs_task_customer').on('click',function(){
            if ($('.jSignature').length){
                $('.jSignature')[0].width = $(window).width()/1.5;
                $('.jSignature')[0].style.width = ""+($(window).width()/1.5)+"px";
                $('.jSignature')[0].parentElement.style.width = ""+($(window).width()/1.5)+"px";
                $('.jSignature')[0].style.height = "170px";
                $('.jSignature')[0].height = 170;
                $('.jSignature')[0].parentElement.style.height = "170px";
            }
        })

        // update consumed quantity on project formulier online form
        $("a.update_qty").on('click',function(e) {
            if (e.currentTarget.className.match('add_qty')){
                var parent_ele = e.currentTarget.parentElement.parentElement;
                var old_val = parent_ele.getElementsByClassName('consumed_qty');
                old_val[0].innerText = parseInt(old_val[0].innerText) + 1;
            }
            else{
                var parent_ele = e.currentTarget.parentElement.parentElement;
                var old_val = parent_ele.getElementsByClassName('consumed_qty');
                if (parseInt(old_val[0].innerText) > 0){
                    old_val[0].innerText = parseInt(old_val[0].innerText) - 1;
                }
            }
        });
        $("a.all_update_qty").on('click',function(e) {
            var parent_ele = e.currentTarget.parentElement.parentElement;
            var consumed_qty = parent_ele.getElementsByClassName('consumed_qty')[0].innerText;
            var record_id = e.currentTarget.getAttribute('value');
            rpc.query({
                route: "/material_update/",
                params:{
                        record_id: record_id,
                        consumed_qty:consumed_qty,
                    },
            }).then(function (data) {
                if (data == false){
                    alert("Quantity already updated");
                }
            });
        });

        // add product line in sale order and material consumed line
        $("a.add_product").on('click',function(e) {
            var product_id = $('select[name="product_id"]').val();
            var consumed_qty = $('input[name="product_qty"]').val();
            var que_id = e.currentTarget.getAttribute('value');
            if (product_id){
                rpc.query({
                    route: "/material_add/",
                    params:{
                            que_id: que_id,
                            product_id: product_id,
                            consumed_qty:consumed_qty,
                        },
                }).then(function (data) {
                    if (data == true){
                        document.location.reload();
                    }
                });
            }
            
        });
    });
});
