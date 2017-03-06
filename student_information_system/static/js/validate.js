"use strict"

$(function(){
    var a = $(".btn-a").val();
    $(".btn-a").next(".hidden-a").val(a);

    $(".hour-input").change(function(event) {
        var h = $(this).val();
        console.log(h);
        if (h < 1) {
            $(this).val('1');
            console.log('error');
        }

        if (h > 12) {
            $(this).val('12');
            console.log('error');
        }
    });

    $(".min-input").change(function(event) {
        var h = $(this).val();
        console.log(h);
        if (h < 0) {
            $(this).val('0');
            console.log('error');
        }

        if (h > 59) {
            $(this).val('59');
            console.log('error');
        }
    });

    $(".btn-a").click(function(event) {
        if ($(this).val() == "AM") {
            $(this).val('PM');
            $(this).next(".hidden-a").val('PM');
        }
        else {
            $(this).val('AM');
            $(this).next().val('a');
            $(this).next(".hidden-a").val('AM');
        }
        event.preventDefault();
    });

});