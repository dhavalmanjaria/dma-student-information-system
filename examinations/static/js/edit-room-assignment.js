$(function() {

    var x = $("input").val();
    console.log(x);

    $("input[name='end_seat']").change(function() {
        var val = $(this).prev("input").val();
        $(this).attr("min", val);
    });

    $("input[name='start_seat']").change(function() {
        var end_seat =  $("input[name='start_seat']");
        var val = end_seat.prev("input").val();
        end_seat.attr("min", val);
    });
    
})