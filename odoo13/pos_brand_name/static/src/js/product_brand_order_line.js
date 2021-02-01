odoo.define('pos_brand_name.product_brand_order_line', function(require) {
    "use strict";

    var models = require('point_of_sale.models');
    var _super_orderline = models.Orderline.prototype;
//    console.log(_super_orderline)

    console.log("hoy")
    models.Orderline=models.Orderline.extend({
        initialize:function(attr,options){
                models.load_fields('product.product',['brand_name_id']);
                var line=_super_orderline.initialize.apply(this,arguments);
                this.brand_name_id=this.product.brand_name_id;



        }
    });
    });

