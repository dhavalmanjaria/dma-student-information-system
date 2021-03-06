$(function() {

    $("#datepicker").datepicker({
        dateFormat: "dd/mm/yy"
    });

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = $.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    $(".select").selectmenu();
    $("#select-course").selectmenu({
        change: function(event, ui) {
            $.ajax({
                url: $("#select-form").attr("action"),
                data: {
                    'course': $(this).val(),
                    'csrfmiddlewaretoken': getCookie('csrftoken')
                },
                success: function(msg) {
                    $("#select-semester").html(msg);
                    $( "#select-semester" ).selectmenu( "refresh" );
                },
                method: 'POST'
            });
        }
    });


    // $("#select-course").change(function() {
    //     console.log('changing course');
    //     // $.ajax({
    //     //     url: $("#select-form").attr("action"),
    //     //     data: $(this).val(),
    //     //     success: function(msg) {
    //     //         $("#select-semester").append(msg);
    //     //     },
    //     //     method: 'POST'
    //     // });
    // });

});