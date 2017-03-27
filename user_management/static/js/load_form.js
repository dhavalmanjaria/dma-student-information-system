"use strict";

$(function() {

    $("#id_group").val(0);

    $("#id_group").selectmenu("option", "change", (function(event) {
        var request = $.ajax({
            url: '/user_management/register',
            data: {'group': $("#id_group").val(),
                },
            method: "GET",
            success: function(msg) {
                $("#second_form").html(msg);
                $("#second_form select").selectmenu();
              //  $("#id_group").val(0);
            },
        });
    }));
})