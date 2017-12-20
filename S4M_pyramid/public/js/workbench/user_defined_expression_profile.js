var below_detection_threshold =  "#808080";
var between_detection_threshold_and_median = "blue";
var above_median = "orange";



function return_colour(value,detection_threshold,median) {

    color = below_detection_threshold;
    if ((value > detection_threshold) && (value < median)){ color = between_detection_threshold_and_median; }
    if (value >= median){ color = above_median; }
    if (value <= detection_threshold) { color = below_detection_threshold; }

    return color;
}

// https://stackoverflow.com/questions/15762768/javascript-math-round-to-two-decimal-places
function roundTo(n, digits) {
 if (digits === undefined) {
   digits = 0;
 }

 var multiplicator = Math.pow(10, digits);
 n = parseFloat((n * multiplicator).toFixed(11));
 var test =(Math.round(n) / multiplicator);
 return +(test.toFixed(digits));
}


$(document).ready(function() {
        var detection_threshold = parseFloat($('#detection_threshold').html())*10;
        var min_value_for_dataset = parseFloat($('#min_value_for_dataset').html())*10;
        var max_value_for_dataset = parseFloat($('#max_value_for_dataset').html())*10;
        var median = parseFloat($('#median').html())*10;

        $("div.slider").slider({
            orientation: "vertical",
            range: "min",
            min:min_value_for_dataset,
            max:max_value_for_dataset,
            value: detection_threshold,
            slide: function( event, ui ) {
                var value_id = '#'+$(this).attr('id').replace('slider','value');
                var input_id = '#'+$(this).attr('id').replace('slider','input');
                var value = ui.value;
                var actual_value = value/10;
                var display_value = roundTo(actual_value, 2);
                $( value_id ).html( display_value );
                $( input_id ).val( actual_value );
                var color = return_colour(value,detection_threshold,median);
                $(this).find('.ui-widget-header').css('background',color);
            }
        });
     
        var initialise_slider = $('#initialise_slider').html();
        if (initialise_slider != ''){
            var slider_values = jQuery.parseJSON(initialise_slider);
            var sample_type_display_order = $('#sample_type_display_order').html();
            if (sample_type_display_order != null){

                sample_type_display_order = sample_type_display_order.split(',');
                for (var position in sample_type_display_order){
                    var sample_type = sample_type_display_order[position];
                    var actual_value =slider_values['expression_values'][sample_type] ;
                    var value = actual_value * 10;
                    var label = '#slider_'+position;
                    $(label).slider('value',value);


                    var display_value = roundTo(actual_value, 2);
                    $('#value_'+position).html(display_value); 
                    var color = return_colour(value,detection_threshold,median);
                    $(label).find('.ui-widget-header').css('background',color);
                    $(label).slider('option','disabled',true);
                }
            }
        }
});

    
