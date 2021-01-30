odoo.define('product_brand.product_brand_js', function(require) {
    "use strict";
    var models = require('point_of_sale.models');
    var _super_orderline = models.Orderline.prototype;
    models .load_fields('product.product','brand_name');
    models.Orderline=models.Orderline.extend({
        export_for_printing:function(session,attributes){
//              models.load_fields('product.product',['brand_name']);
                var line=_super_orderline.export_for_printing.apply(this,arguments)
//              _super_orderline.brand_print.apply(this,arguments);
                line.brand_name=this.get_product().brand_name;
                return line;
//              console.log("hai");

        }
    });
    });

