$(function() {
    $("#id_group").change(function(event) {
        var request = $.ajax({
            url: '/user_management/register',
            data: {'option': $("#id_group option:selected").index(),
                },
            method: "GET",
            success: function(msg) {
                $("#student_info_form").html(msg);
            },
        });
    })
})