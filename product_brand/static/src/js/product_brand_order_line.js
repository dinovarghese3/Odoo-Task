odoo.define('product_brand.product_brand_order_line', function(require) {
    "use strict";

    var models = require('point_of_sale.models');
    var _super_orderline = models.Orderline.prototype;
//    console.log(_super_orderline)
    models.load_fields('product.product','brand_name_id');

    console.log("hoy")
    models.Orderline=models.Orderline.extend({
        initialize:function(attr,options){

                var line=_super_orderline.initialize.apply(this,arguments);
                console.log("line",line);
                console.log(this.product)
                this.brand_name_id=this.product.brand_name_id;
                console.log(this.brand_name_id)
                console.log("line : ",line);
                console.log(this.brand_name_id);


        }
    });
    });

