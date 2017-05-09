"use strict";

$(function() {
    $(".add-button").click(function() {

        var amount = $(this).next('.item_amount').text();
        amount = parseInt(amount);
        var total_amount = $("#pending_amount").val();
        total_amount = parseInt(total_amount);
        total_amount = total_amount + amount;
        $("#pending_amount").val(total_amount);
    })

});