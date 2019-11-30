odoo.define('so_project_formulier_material.screw_piles', function (require) {
'use strict';

    var core = require('web.core');
    var Dialog = require('web.Dialog');
    var Widget = require('web.Widget');
    var rpc = require('web.rpc');
    var QWeb = core.qweb;

    $(document).ready(function () {
        // screw piles update
        $("select[name='screw_piles_ids']").on('change',function(e) {
            var piles_id = e.currentTarget.value
            if (piles_id) {
                rpc.query({
                    model: 'screw.piles',
                    method: 'search_read',
                    domain: [['id', '=', parseInt(piles_id)]],
                    fields: ['sawn_length', 'archived_torque', 'archived_torque','add_work','remarks','image'],
                 }).then(function (data) {
                    $('input[name="sawn_length"]').attr2('value', data[0].sawn_length);
                    $('input[name="archived_torque"]').attr2('value', data[0].archived_torque);
                    $('textarea[name="add_work"]').attr2('value', data[0].add_work || '');
                    $('textarea[name="remarks"]').attr2('value', data[0].remarks || '');
                    $('.screw_image').attr2('src', 'data:image/jpg;base64,'+data[0].image || false);
                });
            }
            if (!piles_id) {
                $('input[name="sawn_length"]').attr2('value', 0);
                $('input[name="archived_torque"]').attr2('value', 0);
                $('textarea[name="add_work"]').attr2('value', '');
                $('textarea[name="remarks"]').attr2('value', '');
                $('.screw_image').attr2('src',false);
            }
        });

        $(".update_screw_piles").on('click',function(e){
            var piles_id = $("select[name='screw_piles_ids']").val();
            var files = $("#image");
            var base64result = false;
            if (files){
                var base64result = files.getAttributes().src.split(',')[1];
            }
            if (piles_id){
                var vals = {'sawn_length': $('input[name="sawn_length"]').val(),
                            'archived_torque': $('input[name="archived_torque"]').val(),
                            'add_work': $('textarea[name="add_work"]').val(),
                            'remarks': $('textarea[name="remarks"]').val(),
                            'image': base64result}
                rpc.query({
                    model: 'screw.piles',
                    method: 'write',
                    args: [[parseInt(piles_id)], vals],
                 }).then(function (data) {
                        alert('Record save successfully!')
                   });
            }
        })
    });
});
