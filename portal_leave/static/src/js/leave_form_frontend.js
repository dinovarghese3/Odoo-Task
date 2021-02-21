odoo.define('portal_leave.leave_form_frontend', function(require) {

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

   //Compute Duration based on start date and end date
    $('#start_date_leave,#end_date_leave').change(function(){

        var diff =new Date($('#end_date_leave').val()) - new Date($('#start_date_leave').val());
        var no_of=(diff/1000/60/60/24);
        console.log("LL",no_of);
        if (no_of <0){
            alert("End date must be grater than start date");
            $('#duration').val(0);
        }
        else{$('#duration').val(no_of+1);}

    });

//  Checking thr half_day check box is checked or not if checked end date,duration hided and time peroid enabled
    $('input[id="half_day"]').click(function(){
            if($(this).prop("checked") == true){
                console.log("Checkbox is checked.");
                $('#end_date_leave').val($('#start_date_leave').val())
                $('#end_date_leave,#end_date_label').hide();
                $('#custom_hours').prop("checked", false);
                $('#time_period').show();
                $('#leave_type_time_off_from,#leave_type_time_off_to,#leave_type_time_off_label').hide();
//                $('#duration_leave_label,#duration').hide();
//                $('#unit_of_duration').hide()
                 $('#unit_of_duration').html("Hours")
                 $('#duration').val("4");
            }
            else if($(this).prop("checked") == false){
                console.log("Checkbox is unchecked.");
                $('#time_period').hide();
                $('#end_date_leave,#end_date_label').show();
                $('#duration_leave_label,#duration').show();
                $('#unit_of_duration').show();
                $('#unit_of_duration').html("Days")
            }
    });

//            Checking Custom hours checked or not
    $('input[id="custom_hours"]').click(function(){
            if($(this).prop("checked") == true){
                console.log("Checkbox is checked.");
                $('#end_date_leave').val($('#start_date_leave').val())
                $('#half_day').prop("checked", false);
                $('#end_date_leave,#end_date_label').hide();
                $('#time_period').hide();
                $('#leave_type_time_off_from,#leave_type_time_off_to,#leave_type_time_off_label').show();
                $('#duration_leave_label,#duration').hide();
                $('#unit_of_duration').hide();
            }
            else if($(this).prop("checked") == false){
                console.log("Checkbox is unchecked.");
                $('#time_period').hide();
                $('#leave_type_time_off_from,#leave_type_time_off_to,#leave_type_time_off_label').hide();
                $('#end_date_leave,#end_date_label').show();
                $('#duration_leave_label,#duration').show();
                $('#unit_of_duration').html("Days")
            }
    });

    $('#leave_type_from,#leave_type_to').change(function(){
        console.log("leave tyoe fun")
        console.log($('#leave_type_from').val())
        console.log($('#leave_type_to').val())
        var duration = $('#leave_type_to').val()
        $('duration').val($('#leave_type_to').val())
    });
//    $('#submit_button').click(function(event){
//        event.preventDefault ? event.preventDefault() : event.returnValue = false;
//        if( ('#duration').val() <=0 ){
//            alert("Check your Dates");
//        }
//
//    })

})