odoo.define('quotation_images_feedback.custom', function (require) {
'use strict';

    var MediaDialog = require('wysiwyg.widgets.MediaDialog')
    var MediaF = require('wysiwyg.widgets.media')
    var core = require('web.core');
    var concurrency = require('web.concurrency');
    var Dialog = require('web.Dialog');
    var Widget = require('web.Widget');
    var rpc = require('web.rpc');
    var QWeb = core.qweb;
    var _t = core._t;

var RecordImageWidget = MediaF.SearchableMediaWidget.extend({

    template: 'quotation_images_feedback.widgets.image',
//     xmlDependencies: Dialog.prototype.xmlDependencies.concat( ['/quotation_images_feedback/static/src/xml/wysiwyg.xml'],
// ),
    events: _.extend({}, MediaF.SearchableMediaWidget.prototype.events || {}, {
        'click .o_existing_attachment_cell': '_onAttachmentClick',
        'dblclick .o_existing_attachment_cell': '_onAttachmentDblClick',
    }),

    NUMBER_OF_ATTACHMENTS_TO_DISPLAY: 30,

    init: function (parent, media, options) {
        this._super.apply(this, arguments);
        this._mutex = new concurrency.Mutex();
        this.numberOfAttachmentsToDisplay = this.NUMBER_OF_ATTACHMENTS_TO_DISPLAY;
        this.options = _.extend({
            firstFilters: [],
            lastFilters: [],
        }, options || {});
        this.selectedAttachments = [];
    },

    willStart: function () {
        return Promise.all([
            this._super.apply(this, arguments),
            this.search('', true)
        ]);
    },

    start: function () {
        var def = this._super.apply(this, arguments);
        var self = this;
        this._renderImages();
        return def;
    },

    save: function () {
        return this._mutex.exec(this._save.bind(this));
    },

    search: function (needle, noRender) {
        var self = this;
        return this._rpc({
            route: "/sale_order/project_formulier/get",
            params: {
                order_id: parseInt(self.options.res_id),
                res_model: self.options.res_model,
            },
        }).then(function (data) {
            self.records = data;
            if (!noRender) {
                self._renderImages();
            }
        });
    },

    _highlightSelected: function () {
        var self = this;
        this.$('.o_existing_attachment_cell.o_we_attachment_selected').removeClass("o_we_attachment_selected");
        _.each(this.selectedAttachments, function (attachment) {
            self.$('.o_existing_attachment_cell[data-id=' + attachment + ']').addClass("o_we_attachment_selected");
        });
    },

    _clear: function () {
        if (!this.$media.is('img')) {
            return;
        }
        this.media.className = "img img-fluid";
    },
    _renderImages: function () {
        var self = this;
        if (this.options.document){
            this.$('div.record-data').html(
                QWeb.render('quotation_images_feedback.widgets.document.existing.attachments',{
                    rows: this.records,
                    widget: this,
                })
            );
        }
        else if (this.options.video){
            this.$('div.record-data').html(
                QWeb.render('quotation_images_feedback.widgets.video.existing.attachments',{
                    rows: this.records,
                    widget: this,
                })
            );
        }
        else{
            this.$('div.record-data').html(
                QWeb.render('quotation_images_feedback.widgets.image.existing.attachments',{
                    rows: this.records,
                    widget: this,
                })
            );
        }
        this._highlightSelected();
    },

    _save: function () {
        var self = this;
        var data = this.selectedAttachments
        if (this.options.video){
                var video = _.find(this.records['video_ids'], function (record) {
                    return record[0] === data[0];
                });
                var v_tag = $('<video src="/web/video/'+video[0]+'" title="'+video[1]+'" class="col-lg-12 col-md-12" controls="" ></video>');
                return this.media = v_tag[0];
        }
        if (this.options.document){
                var doc = _.find(this.records['document_ids'], function (record) {
                    return record[0] === data[0];
                });
                var a_tag = $('<a href="/web/content?model=order.document&field=file&id='+doc[0]+'&filename='+doc[1]+'download=true" class="col-lg-12 col-md-12" target="_blank"><span class="fa fa-file" style="font-size:80px;"></span><p style="word-wrap: break-word;>'+doc[1]+'</p></a>');
                this.media = a_tag[0];
        }
        else{
            var img = $("img[data-id='"+this.selectedAttachments+"']");
            this.media.src=img[0].src;
        }
        return this.media
    },

    _selectAttachement: function (attachment, save) {
        if (this.multiImages) {
            var index = this.selectedAttachments.indexOf(attachment);
            if (index != -1) {
                if (!save) {
                    this.selectedAttachments.splice(index, 1);
                }
            } else {
                this.selectedAttachments.push(attachment);
            }
        } else {
            this.selectedAttachments = [attachment];
        }
        this._highlightSelected();
        if (save) {
            this.trigger_up('save_request');
        }
    },

    _onAttachmentClick: function (ev, save) {
        var $attachment = $(ev.currentTarget);
        if (this.options.video) {
            var attachment = _.find(this.records['video_ids'], function (record) {
                    return record[0] === $attachment.data('id');
                })[0];
        }
        else if (this.options.document) {
            var attachment = _.find(this.records['document_ids'], function (record) {
                    return record[0] === $attachment.data('id');
                })[0];
        }
        else {
            if (typeof($attachment.data('id')) === "string"){
                var attachment = _.find(this.records['data'], function (record) {
                    return record === $attachment.data('id');
                });
            }
            if (typeof($attachment.data('id')) === "number") {
                var attachment = _.find(this.records['image_ids'][0], function (record) {
                    return record === $attachment.data('id');
                });
            }
             
        }
        this._selectAttachement(attachment, save);
    },

    _onAttachmentDblClick: function (ev) {
        this._onAttachmentClick(ev, true);
    },
});

MediaDialog.include({
    template: 'wysiwyg.widgets.media',
    xmlDependencies: Dialog.prototype.xmlDependencies.concat(
            ['/quotation_images_feedback/static/src/xml/wysiwyg.xml']
        ),
    events: _.extend({}, Dialog.prototype.events, {
        'click #editor-media-image-tab': '_onClickImageTab',
        'click #editor-media-document-tab': '_onClickDocumentTab',
        'click #editor-media-icon-tab': '_onClickIconTab',
        'click #editor-media-video-tab': '_onClickVideoTab',
        'click #editor-media-record_image-tab': '_onClickRecordImageTab',
        'click #editor-media-record_document-tab': '_onClickRecordDocumentTab',
        'click #editor-media-record_video-tab': '_onClickRecordVideoTab',
    }),

    init: function (parent, options, media) {
        var self = this;
        this.media = media;
        this.$media = $(media);
        var onlyImages = options.onlyImages || this.multiImages || (this.media && (this.$media.parent().data('oeField') === 'image' || this.$media.parent().data('oeType') === 'image'));
        options.noRecordImages = onlyImages || options.noRecordImages
        options.noRecordDocuments = onlyImages || options.noRecordDocuments;
        options.noRecordVideos = onlyImages || options.noRecordVideos;
        this._super(parent, _.extend({}, {
            title: _t("Select a Media"),
            save_text: _t("Add"),
        }, options));

        this.trigger_up('getRecordInfo', {
            recordInfo: options,
            type: 'media',
            callback: function (recordInfo) {
                _.defaults(options, recordInfo);
            },
        });

        if(options.res_model == 'sale.order.template'){
            if (!options.noRecordVideos) {
                this.record_videoWidget = new RecordImageWidget(this, this.media, _.extend({}, options, {video: true}));
            }
        }
        if(options.res_model == 'sale.order'){
            if (!options.noRecordImages) {
                this.record_imageWidget = new RecordImageWidget(this, this.media, options);
            }
            if (!options.noRecordDocuments) {
                this.record_documentWidget = new RecordImageWidget(this, this.media, _.extend({}, options, {document: true}));
            }
            if (!options.noRecordVideos) {
                this.record_videoWidget = new RecordImageWidget(this, this.media, _.extend({}, options, {video: true}));
            }
        }
    },
    start: function () {
        var promises = [this._super.apply(this, arguments)];
        this.$el.find('#editor-media-record_image-tab').hide();
        this.$el.find('#editor-media-record_video-tab').hide();
        this.$el.find('#editor-media-record_document-tab').hide();

        if (this.record_imageWidget) {
            this.$el.find('#editor-media-record_image-tab').show();
            promises.push(this.record_imageWidget.appendTo(this.$("#editor-media-record_image")));
        }
        if (this.record_documentWidget) {
            this.$el.find('#editor-media-record_document-tab').show();
            promises.push(this.record_documentWidget.appendTo(this.$("#editor-media-record_document")));
        }
        if (this.record_videoWidget) {
            this.$el.find('#editor-media-record_video-tab').show();
            promises.push(this.record_videoWidget.appendTo(this.$("#editor-media-record_video")));
        }
        return Promise.all(promises);
    },
    

    isRecordImageActive: function () {
        return this.activeWidget === this.record_imageWidget;
    },
    isRecordDocumentActive: function () {
        return this.activeWidget === this.record_documentWidget;
    },
    isRecordVideoActive: function () {
        return this.activeWidget === this.record_videoWidget;
    },

    _onClickRecordImageTab: function () {
        this.activeWidget = this.record_imageWidget;
    },
    _onClickRecordDocumentTab: function () {
        this.activeWidget = this.record_documentWidget;
    },
    _onClickRecordVideoTab: function () {
        this.activeWidget = this.record_videoWidget;
    },

    _clearWidgets: function () {
        [   this.imageWidget,
            this.documentWidget,
            this.iconWidget,
            this.videoWidget,
            this.record_imageWidget,
            this.record_documentWidget,
            this.record_videoWidget
        ].forEach( (widget) => {
            if (widget !== this.activeWidget) {
                widget && widget.clear();
            }
        });
    },
});
});
