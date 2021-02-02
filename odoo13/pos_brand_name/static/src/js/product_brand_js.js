odoo.define('pos_brand_name.product_brand_js', function(require) {
    "use strict";

//  To Add Brand Name in Receipt
    var models = require('point_of_sale.models');
    models.load_fields('product.product','brand_name_id');
    var _super_orderline = models.Orderline.prototype;
    console.log("hai")

    models.Orderline=models.Orderline.extend({
        export_for_printing:function(session,attributes){
        console.log("hoy")
                var line=_super_orderline.export_for_printing.apply(this,arguments);
                line.brand_name_id=this.get_product().brand_name_id;
                console.log(line.brand_name_id)
                return line;


        }
    });
    });

