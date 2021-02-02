odoo.define('pos_product_video.pos_product_video',function(require){
    var models = require('point_of_sale.models')
    models.load_fields('product.product','product_video');
    var _super_posmodel = models.PosModel.prototype;
    console.log("Video")
    models.PosModel = models.PosModel.extend({
        initialize: function(session, attributes){
            console.log("video function")
            models.load_fields('product.product','product_video');
            console.log(models.load_fields('product.product','product_video'))
            _super_posmodel.initialize.apply(this, arguments);

        }
    });
});



