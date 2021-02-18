odoo.define('portal_leave.leave_form_frontend', function(require) {



//$('document').ready(function(){
//            if($('#leave_type_time_off').val() == "Compensatory Days"){
//            $('#half_day_leave_type').hide();
//            alert("hai");
//            }
//    })
    $('#half_day_leave_type').hide();
    $('#time_period').hide()
    $('#leave_type_time_off_from,#leave_type_time_off_to,#leave_type_time_off_label').hide();
    console.log("Hai")
    $('#leave_type_time_off_from_other_model').change(function(){
    if (($('#leave_type_time_off_from_other_model').val() == 'Compensatory Days')||($('#leave_type_time_off_from_other_model').val() == 'Unpaid')){
        $('#half_day_leave_type').show();
        $('#end_date_leave').show();
        $('custom_hours').show()
    }
    else{
    $('#half_day_leave_type').hide();
    $('#end_date_leave').show();
    $('custom_hours').hide()
    }
    });
//    $('#end_date_leave').change(function(){
//    console.log($('#end_date_leave').val())
//    console.log(Math.round(($('#end_date_leave').val()-$('#start_date_leave').val())/(1000*60*60*24)));
//        $('#duration').val($('#end_date_leave').val());
//
//    });
    $('#start_date_leave,#end_date_leave').change(function(){

    var diff =new Date($('#end_date_leave').val()) - new Date($('#start_date_leave').val());
    var no_of=(diff/1000/60/60/24);
    console.log("LL",no_of);
        $('#duration').val(no_of+1);

    });
    $('input[id="half_day"]').click(function(){
            if($(this).prop("checked") == true){
                console.log("Checkbox is checked.");
                $('#end_date_leave,#end_date_label').hide();
                $('#custom_hours').prop("checked", false);
                $('#time_period').show();
                $('#leave_type_time_off_from,#leave_type_time_off_to,#leave_type_time_off_label').hide();
                $('#duration_leave_label,#duration').hide();
            }
            else if($(this).prop("checked") == false){
                console.log("Checkbox is unchecked.");
                $('#time_period').hide();
                $('#end_date_leave,#end_date_label').show();
                $('#duration_leave_label,#duration').show();

            }
            });
//    $('#half_day_leave_type').change(function(){
//        $('#end_date_leave').show();
//        if ($('#half_day_leave_type').val !=1 ){
//        console.log("0")
//            $('#end_date_leave').show();
//        }
//    });
$('input[id="custom_hours"]').click(function(){
            if($(this).prop("checked") == true){
                console.log("Checkbox is checked.");
                $('#half_day').prop("checked", false);
                $('#end_date_leave,#end_date_label').hide();
                $('#time_period').hide();
                $('#leave_type_time_off_from,#leave_type_time_off_to,#leave_type_time_off_label').show();
                $('#duration_leave_label,#duration').hide();

            }
            else if($(this).prop("checked") == false){
                console.log("Checkbox is unchecked.");
                $('#time_period').hide();
                $('#leave_type_time_off_from,#leave_type_time_off_to,#leave_type_time_off_label').hide();
                $('#end_date_leave,#end_date_label').show();
                $('#duration_leave_label,#duration').show();

            }
            });

})