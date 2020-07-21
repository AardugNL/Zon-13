odoo.define('project_task_resource_kanban.kanban_view', function (require) {
    "use strict";

    var core = require('web.core');
    var _t = core._t;
    var QWeb = core.qweb;
    var KanbanRecord = require('web.KanbanRecord');
    var KanbanColumn = require("web.KanbanColumn");
    var ControlPanelRenderer = require('web.ControlPanelRenderer');
    // var SearchView = require('web.SearchView');

    // SearchView.include({
    //     willStart: function () {
    //         var self = this;
    //         if (this.action.res_model == "task.resource"){
    //             this.options.disable_filters = true;
    //             // this.options.disable_groupby = true;
    //         }
    //         // var disable_menu = this.fields_view.arch.attrs.disable_menu;
    //         // disable_menu = disable_menu ? disable_menu.split(',') : [];
    //         // _.each(disable_menu, function (menu) {
    //         //     self.options['disable_' + menu] = true;
    //         // });
    //         return $.when(this._super());
    //     },
    // });

    ControlPanelRenderer.include({
        _renderSearch: function () {
            this._super.apply(this, arguments);
            if (this.action.res_model == "task.resource") {
                setTimeout(function(){
                    $('.o_filters_menu_button').addClass('o_hidden');
                }, 500);
            }
        },
    })

    KanbanRecord.include({
        _render: function () {
            if (this.modelName === 'task.resource') {
                this.defs = [];
                this._replaceElement(this.qweb.render('kanban-box', this.qweb_context));
                this.$el.addClass('o_kanban_record').attr("tabindex",0);
                this.$el.attr('role', 'article');
                this.$el.data('record', this);
                if (this.$el.hasClass('oe_kanban_global_click') ||
                    this.$el.hasClass('oe_kanban_global_click_edit')) {
                    this.$el.on('dblclick', this.on_card_dblclicked.bind(this));
                    this.$el.on('keydown', this._onKeyDownCard.bind(this));
                } else {
                    this.$el.on('keydown', this._onKeyDownOpenFirstLink.bind(this));
                }
                this._processFields();
                this._processWidgets();
                this._setupColor();
                this._setupColorPicker();
                this._attachTooltip();

                // We use boostrap tooltips for better and faster display
                this.$('span.o_tag').tooltip({delay: {'show': 50}});

                return $.when.apply(this, this.defs);
            } else {
                this._super.apply(this, arguments);
            }
        },

        on_card_dblclicked: function() {
            if (this.modelName === 'task.resource') {
                if(this.record.obj_type.raw_value == 'task'){
                    var action = {
                        type: 'ir.actions.act_window',
                        res_model: 'project.task',
                        view_mode: 'form',
                        view_type: 'form',
                        views: [[false, 'form']],
                        target:'new',
                        res_id: this.record.task_id.raw_value
                    };
                    this.do_action(action);
                }
                if(this.record.obj_type.raw_value == 'resource'){
                    var action = {
                        type: 'ir.actions.act_window',
                        res_model: 'resource.resource',
                        view_mode: 'form',
                        view_type: 'form',
                        views: [[false, 'form']],
                        target:'new',
                        res_id: this.record.resource_id.raw_value
                    };
                    this.do_action(action);
                }
            }
        },
    });

    KanbanColumn.include({
        init: function () {
            this._super.apply(this, arguments);
            if (this.modelName === 'task.resource') {
                this.draggable = false;
            }
        },
        start: function() {
            var self = this;
            this._super.apply(this, arguments);
            if (this.modelName === 'task.resource') {
                setTimeout(function(){
                this.drag = this.$('.kanban_draggable');
                this.drop = this.$('.kanban_droppable');
                this.drop.draggable({ revert: "invalid",
                    refreshPositions: true,
                    connectWith: '.kanban_draggable',
                    delay: 0,
                    items: '> .o_kanban_record:not(.o_updating)',
                    cursor: 'move',
                });
                this.drag.droppable({
                    drop: function(event, ui){
                        event.preventDefault();
                        var record = ui.draggable.data('record');
                        ui.draggable.addClass('o_updating');
                        var data = {};
                        data['dragged-task'] = record.id;
                        data['resource-id'] = parseInt(event.target.dataset.id);
                        self._rpc({
                            model: 'task.resource',
                            method: 'update_task_resource',
                            args: [parseInt(event.target.dataset.id), data],
                        }).then(function() {
                            window.location.reload();
                        });
                        ui.draggable.hide();
                    }
                });
                this.drag.draggable({
                    revert: "invalid",
                    refreshPositions: true,
                    connectWith: '.kanban_droppable',
                    delay: 0,
                    items: '> .o_kanban_record:not(.o_updating)',
                    cursor: 'move',
                    drag: function(event, ui){
                        ui.helper.css({"z-index": "1000"});
                    },
                    stop: function (event, ui) {
                        ui.helper.css({"z-index": "auto"});
                    }
                });
                this.drop.droppable({
                    drop: function( event, ui ) {
                        event.preventDefault();
                        var record = ui.draggable.data('record');

                        ui.draggable.addClass('o_updating');
                        var data = {};
                        data['dragged-resource'] = record.id;
                        data['task-id'] = parseInt(event.target.dataset.id);
                        self._rpc({
                            model: 'task.resource',
                            method: 'update_task_resource',
                            args: [parseInt(event.target.dataset.id), data],
                        }).then(function() {
                            window.location.reload();
                        });
                        ui.draggable.hide();
                    }
                });
            }, 500);
            }
        },
    });
});