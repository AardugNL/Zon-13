odoo.define('quotation_images_feedback.image_upload', function (require) {
'use strict';

    var core = require('web.core');
    var Dialog = require('web.Dialog');
    var Widget = require('web.Widget');
    var rpc = require('web.rpc');
    var QWeb = core.qweb;

    $(document).ready(function () {

        var task_op = $('#nav_tabs_task_op_form');
        var quote_op = $('#nav_tabs_quote_op_form');
        var task_op_image = $('#nav_tabs_task_op_image_form');
        var task_op_extra_image = $('#nav_tabs_task_op_extra_image_form');
        var task_op_video = $('#nav_tabs_task_op_video_form');
        
        if (task_op.length > 0){
            var inputs = task_op[0].querySelectorAll('input,select,textarea')
            inputs.forEach(function(element) {
                element.disabled='true';
            });
        }
        if (quote_op.length > 0){
            var inputs = quote_op[0].querySelectorAll('input,select,textarea')
            inputs.forEach(function(element) {
                element.disabled='true';
            });
        }
        if (task_op_image.length > 0){
            var inputs = task_op_image[0].querySelectorAll('input')
            inputs.forEach(function(element) {
                $('#'+element.name).prev().hide();
            });
        }
        if (task_op_extra_image.length > 0){
            var inputs = task_op_extra_image[0].querySelectorAll('button')
            var upload = task_op_extra_image[0].querySelectorAll('.custom-file-upload')
            upload[0].parentElement.hidden = true
            inputs.forEach(function(element) {
                element.hidden='true';
            });
        }
        if (task_op_video.length > 0){
            var inputs = task_op_video[0].querySelectorAll('button')
            var upload = task_op_video[0].querySelectorAll('.custom-file-upload')
            upload[0].parentElement.hidden = true
            inputs.forEach(function(element) {
                element.hidden='true';
            });
        }

        // edit images field on question/formulier/id
        $('.edit_button').on('click', function (e) {
            var file_input = $('input[name="'+e.currentTarget.nextElementSibling.id+'"]')
            file_input.click();
            e.preventDefault();
            file_input.on('change', function(e){
                var file = this.files[0];;
                var currentImg = $('img[id="'+e.currentTarget.name+'"]');
                currentImg.after($('<span class="text-success">Uploading....</span>'))
                var reader = new FileReader();
                reader.onloadend = function() {
                    var data=(reader.result).split(',')[1];
                    var write_values = {};
                    write_values[e.currentTarget.name] = data;
                    currentImg[0].src=reader.result;
                    rpc.query({
                        model: 'question.formulier',
                        method: 'write',
                        args: [[parseInt($('input[name="que_id"]').val())],
                                    write_values],
                     }).then(function (data) {
                        currentImg.next()[0].replaceWith($('<span class="text-success">Image uploaded successfully</span>')[0]);
                    });
                }
                reader.readAsDataURL(file);
            });
        });

         $("form img").on('click mouseenter',function(e){
            var curr_img = e.currentTarget;
            curr_img.style="opacity:0.4";
            var search_icon = $('<span class="fa fa-search image_zoom"></span>')[0];
            curr_img.after(search_icon);
            $(curr_img).on('click',function(event){
                $(event.currentTarget).addClass('img_zoom');
                event.currentTarget.style="opacity:1";
                search_icon.remove();
            });
         });
         $("form img").on('mouseleave',function(e){
            var curr_img = e.currentTarget;
            curr_img.style="opacity:1";
            if (curr_img.nextElementSibling.className.includes('image_zoom')){
                curr_img.nextElementSibling.remove();
            }
            $(curr_img).removeClass('img_zoom');
         });
    });
    
});