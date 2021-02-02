odoo.define('product_brand.product_brand_js', function(require) {
    "use strict";

//    To Add Brand Name in  Receipt
    var models = require('point_of_sale.models');
    var _super_orderline = models.Orderline.prototype;
    models .load_fields('product.product','brand_name_id');
    models.Orderline=models.Orderline.extend({
        export_for_printing:function(session,attributes){

                var line=_super_orderline.export_for_printing.apply(this,arguments);
                line.brand_name=this.get_product().brand_name_id;
                line.brand_name_id=this.get_product().brand_name_id;
                console.log(line)
                return line;

        }
    });
    });

