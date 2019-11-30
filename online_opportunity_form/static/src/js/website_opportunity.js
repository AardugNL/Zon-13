odoo.define('online_opportunity_form.opportunity', function (require) {
    "use strict";

    var ajax = require('web.ajax');

    $( document ).ready(function() {
        $('#loading').hide();
        $(this).on('click', ".o_website_opportunity", function (e) {
            $('#loading').show();
            var allData = {
                'title': parseInt($("select[name='title']").val()),
                'lead_category': parseInt($("select[name='lead_category']").val()),
                'question_type': $("select[name='question_type']").val(),
                'first_name': $("#first_name").val(),
                'last_name': $("#last_name").val(),
                'street': $("#street").val(),
                'zip': $("#zip").val(),
                'city': $("#city").val(),
                'country': parseInt($("select[name='country']").val()),
                'phone': $("#phone").val(),
                'email': $("#email").val(),
                'lead_lead_source': parseInt($("select[name='lead_lead_source']").val()),
            }
            ajax.jsonRpc("/opportunity/create", 'call', {
                            'data': allData,
                }).then(
                    function(data) {
                        $('#loading').hide();
                        window.open(data.url, '_self');
                });
        });
    });
});