odoo.define('pos_product_video.pos_product_video', function (require) {
    "use strict";
    var core = require('web.core');
    var screens = require('point_of_sale.screens');
    var models = require('point_of_sale.models');
    var gui = require('point_of_sale.gui');
    var PopupWidget = require('point_of_sale.popups');

    var rpc = require('web.rpc');
    var QWeb = core.qweb;
    var _t = core._t;
    models.load_fields('product.product','product_video');
//    models.load_fields('product.product', 'embed_code');


//this.el.querySelector('.search-clear.right').addEventListener('click',this.clear_search_handler);
var PosProductVideoPopupWidget = PopupWidget.extend({
        template: 'ProductVideoPopupWidget',
});
gui.define_popup({name:'product_video_show', widget: PosProductVideoPopupWidget});


screens.ProductListWidget.include({

    init: function(parent, options) {
        var self = this;
//        console.log("this:",this)
//        console.log("self:",self)
//        console.log("HOOOO",options)
        this._super(parent,options);

        this.click_product_handler = function(ev){
            if (ev.target.className == "fa fa-play"){
                var product = self.pos.db.get_product_by_id(this.dataset.productId);
                console.log("product::",product)
//                   alert("hai")
                self.pos.gui.show_popup('product_video_show', {
                'title':_t('Video'),
                'value':false,
                "body": product.embed_code,
                });


            }else{
               console.log("111",ev.target.className)
            var product = self.pos.db.get_product_by_id(this.dataset.productId);

            options.click_product_action(product);
            }
        };


    },



});


});