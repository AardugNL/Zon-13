odoo.define('formulier_image_url.image_upload', function (require) {
    'use strict';

        var ajax = require('web.ajax');

        $(document).ready(function () {
            function convertFileToDataURLviaFileReader(url, callback) {
                var xhr = new XMLHttpRequest();
                xhr.onload = function() {
                  var reader = new FileReader();
                  reader.onloadend = function() {
                    callback(reader.result);
                  }
                  reader.readAsDataURL(xhr.response);
                };
                xhr.open('GET', url);
                xhr.responseType = 'blob';
                xhr.send();
            }

            $('.edit_from_url').on('click', function(event){
                var id = $(this).attr('rid');
                var convertType = 'FileReader';
                var imageUrl = $('#urlname').val();
                if (imageUrl == 'undefined')
                {
                    $('.close_modal').trigger('click');
                }
                var convertFunction = convertType === 'FileReader' ?
                  convertFileToDataURLviaFileReader :
                  convertImgToDataURLviaCanvas;
                convertFunction(imageUrl, function(base64Img) {
                    var base64result = base64Img.split(',')[1];
                    var response = base64Img.split(',')[0];
                    if(id && response != 'data:text/html;base64'){
                        $('img[id=image]').attr('src', base64Img);
                        ajax.jsonRpc('/web/dataset/call_kw', 'call', {
                          "args": [
                            [parseInt(id)], {
                              "image": base64result,
                            }
                          ],
                          "model": "question.formulier",
                          "method": "write",
                          "kwargs": {
                            "context": {
                            }
                          }
                        });
                    }
                });
              $('#UrlLinkModal').modal('toggle');
            });
        });
    });
