odoo.define('product_brand.product_brand_js', function(require) {
    "use strict";
//    To Add Brand Name in  Receipt
    var models = require('point_of_sale.models');
    var _super_orderline = models.Orderline.prototype;
    models .load_fields('product.product','brand_name_id');
    models.Orderline=models.Orderline.extend({
        export_for_printing:function(session,attributes){
            var line=_super_orderline.export_for_printing.apply(this,arguments);
            console.log(this.get_product().brand_name_id[1])
            if (this.get_product().brand_name_id[1]){
                line.product_name_wrapped.push("(Brand:"+this.get_product().brand_name_id[1]+")");}
            return line;}
    });
});

