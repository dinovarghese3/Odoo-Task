odoo.define('pos_product_video.pos_product_video', function(require) {

    const { Gui } = require('point_of_sale.Gui');
    const ProductItem = require('point_of_sale.ProductItem');
    const Registries = require('point_of_sale.Registries');
    const AbstractAwaitablePopup = require('point_of_sale.AbstractAwaitablePopup');
    var models =require('point_of_sale.models');
    var core = require('web.core');
    models.load_fields("product.product", ["product_video_url"]);
    var _t = core._t;
    var rpc = require('web.rpc');
    var pVideo;
    console.log("wrk");

    const PosProductVideo = ProductItem => class extends ProductItem{
        playVideo(ev){
            ev.stopPropagation();
            console.log(this.props.product.product_video_url)
            this.pVideo=this.props.product.product_video_url;
            if (this.props.product.product_video_url){
                if  ((this.props.product.product_video_url.includes('https') || this.props.product.product_video_url.includes('Https'))!=1){
                            this.pVideo="https://"+this.props.product.product_video_url;};
//                            Checking Rguler url or embed url
                if  ((this.props.product.product_video_url.includes('embed'))!=1)
                {
                    var splitUrl= this.props.product.product_video_url.split('/');
                    this.pVideo="https://www.youtube.com/embed/"+splitUrl[3].replace("watch?v=","").split("&")[0];};
//                console.log(this.props.product.product_video_url)
                Gui.showPopup("ProductVideoPopup", {
                    videoUrl: _t(this.pVideo+"?autoplay=1"),
                    title: _t("Product Video"),
                    confirmText: _t("Exit")
                });

            }

        }

    }
    class ProductVideoPopup extends AbstractAwaitablePopup {}
    ProductVideoPopup.template = 'ProductVideoPopup';
    ProductVideoPopup.defaultProps = {
        confirmText: 'Ok',
        videoUrl: '',
        cancelText: 'Cancel',
        title: 'Product Video',
        body: '',
    };
    Registries.Component.add(ProductVideoPopup);
    Registries.Component.extend(ProductItem, PosProductVideo);
    return PosProductVideo,ProductVideoPopup;

});