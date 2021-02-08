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
    models.load_fields('pos.config','product_video_enable')

var PosProductVideoPopupWidget = PopupWidget.extend({
//PopUp widget Function
        template: 'ProductVideoPopupWidget',
        show: function(options){
                        options = options || {};
                        var self = this;
                        this._super(options);
//                        console.log("video====",options.ProductVideo)
                        this.pVideo = options.ProductVideo+"?rel=0;autoplay=1;";
//                        Checking  https url or not
                        if  ((options.ProductVideo.includes('https') || options.ProductVideo.includes('Https'))!=1){
                            this.pVideo="https://"+options.ProductVideo+"?rel=0;autoplay=1;";};
//                            Checking Rguler url or embed url
                        if  ((options.ProductVideo.includes('embed'))!=1)
                        {
                            var splitUrl= options.ProductVideo.split('/');
//                            console.log(splitUrl);
                            this.pVideo="https://www.youtube.com/embed/"+splitUrl[3].replace("watch?v=","").split("&")[0]+"?rel=0;autoplay=1;";};
//                            console.log(this.pVideo)
                            this.renderElement();
                    }
});
gui.define_popup({name:'product_video_show', widget: PosProductVideoPopupWidget});

screens.ProductListWidget.include({

//    Function to return the Product video Url
    get_product_video_link: function(product){
        return product.product_video;
    },


    init: function(parent, options) {
        var self = this;
        this._super(parent,options);
//Video icon click
        this.click_product_handler = function(ev){
//        checking the class of the button press event
            if (ev.target.className == "fa fa-play"){
                var product = self.pos.db.get_product_by_id(this.dataset.productId);
                console.log("product::",product)
                    var pVideo = self.get_product_video_link(product);
//                    Calling the popup function
                self.pos.gui.show_popup('product_video_show', {
                'ProductVideo':pVideo,
                'title':_t('Video'),
                'value':false,
                "body": product,
                });
            }else{
            var product = self.pos.db.get_product_by_id(this.dataset.productId);
            options.click_product_action(product);
            }
        };

    },

});
});