odoo.define('formulier_type_1.custom', function (require) {
'use strict';

    $(document).ready(function () {
        formulier_type_one();
        var note_show = $("#note_show");
        if (note_show.length){
            note_show[0].disabled=false;
        }
        $('#note_show').on('click', function(e){
            if (e.currentTarget.checked == true){
                $("textarea[name='note']")[0].disabled=false;
                $('.note_field')[0].style.display = 'flex';
            }
            else{
                $('.note_field')[0].style.display = 'none';
            }
        })
    });
});