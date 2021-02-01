odoo.define('product_brand.product_brand_js', function(require) {
    "use strict";


    var models = require('point_of_sale.models');
    var _super_orderline = models.Orderline.prototype;
//    console.log(_super_orderline)
    models .load_fields('product.product','brand_name_id');
    console.log("hoy")
    models.Orderline=models.Orderline.extend({
        export_for_printing:function(session,attributes){
              models.load_fields('product.product',['brand_name']);

                var line=_super_orderline.export_for_printing.apply(this,arguments);
                line.brand_name=this.get_product().brand_name_id;
                console.log(line);
//              _super_orderline.brand_print.apply(this,arguments);
                line.brand_name_id=this.get_product().brand_name_id;
                console.log("line : ",line);
                console.log("hai");
                return line;
//                models.load_fields('product.product',['brand_name_id']);
//                var line=_super_orderline.export_for_printing.apply(this,arguments);
//                this.brand_name_id=this.product.brand_name_id;
//                console.log(this.brand_name_id[1]);


        }
    });
    });

