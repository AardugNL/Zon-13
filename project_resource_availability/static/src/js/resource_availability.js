odoo.define('resource_management.resource_availability', function (require){
    "use strict";

    var core = require('web.core');
    var QWeb = core.qweb;
    var widgetRegistry = require('web.widget_registry');
    var Widget = require('web.Widget');

    var ResourceAvailable = Widget.extend({
        template: "resourceDetails",
        events: {
            'click .search-data': '_onFieldChanged',
        },

        init: function(parent, data, options) {
            this._super.apply(this, arguments);
            this.parent = parent;
            this.resource_header = py.eval(data.data.resource_header);
            this.resource_info = py.eval(data.data.resource_info);
            this.resource_header_date = py.eval(data.data.resource_header_date);
            this.resource_header_day = py.eval(data.data.resource_header_day);
        },

        start: function() {
            this.load_date();
            this.view_loading();
            this.view_free();
            this.view_leave();
            this.view_resources();
            return this._super.apply(this, arguments);
        },

        _onFieldChanged: function () {
            var data = this.parent.state.data;
            this.resource_header = py.eval(data.resource_header);
            this.resource_info = py.eval(data.resource_info);
            this.resource_header_date = py.eval(data.resource_header_date);
            this.resource_header_day = py.eval(data.resource_header_day);
            this.renderElement();
            this.load_date();
            this.view_loading();
            this.view_free();
            this.view_leave();
            this.view_resources();
        },

        view_loading: function(r) {
            return this.load_occupied(r);
        },

        view_free: function(r) {
            return this.load_free(r);
        },

        view_leave: function(r) {
            return this.load_leave(r);
        },

        view_resources: function(r){
            return this.load_resources(r);
        },

        load_date: function(data) {
            var self = this;
            this.$el.find(".table_header_date").bind("click", function(event){
                self.do_action({
                    name: 'Schedule Report',
                    res_model: "schedule.report",
                    views: [[false, 'form']],
                    type: 'ir.actions.act_window',
                    context: {'click_date': event.currentTarget.dataset.date},
                    target: 'new',
                });
            });
        },

        load_occupied: function(data) {
            var self = this;
            this.$el.find(".resource_occupied").bind("click", function(event){
                self.do_action({
                    type: 'ir.actions.act_window',
                    res_model: "task.schedule",
                    views: [[false, 'form']],
                    context: {'click_date': this.dataset.date},
                    res_id: parseInt(event.currentTarget.dataset.id),
                    target: 'new',
                });
            });
        },

        load_free: function(data) {
            var self =  this;
            this.$el.find(".resource_free").bind("click", function(event){
                self.do_action({
                    type: 'ir.actions.act_window',
                    res_model: "summary.report",
                    views: [[this.dataset.view_id, 'form']],
                    context: {'click_date': this.dataset.date},
                    target: 'new',
                });
            });
        },

        load_leave: function(data) {
            var self = this;
            this.$el.find(".resource_leave").bind("click", function(event){
                self.do_action({
                    type: 'ir.actions.act_window',
                    res_model: "summary.report",
                    views: [[false, 'form']],
                    context: {'click_date': this.dataset.date},
                    res_id: parseInt(event.currentTarget.dataset.id),
                    target: 'new',
                });
            });
        },

        load_resources: function(data){
            var self = this;
            this.$el.find(".resource-details").bind("click", function(event){
                self.do_action({
                    type: 'ir.actions.act_window',
                    res_model: "resource.resource",
                    views: [[false, 'form']],
                    res_id: parseInt(event.currentTarget.dataset.id),
                    target: 'new',
                });
            });
        },

        renderElement: function() {
            var $el;
            $el = $(QWeb.render("resourceDetails", {widget: this}).trim());
            this._replaceElement($el);
        }
    });
    widgetRegistry.add('Resource_Availability', ResourceAvailable);
});
