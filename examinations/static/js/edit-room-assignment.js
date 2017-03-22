$(function() {

    var x = $("input").val();
    console.log(x);

    $("input[name='end_seat']").change(function() {
        var val = $(this).prev("input").val();
        $(this).attr("min", val);
    });
    
})