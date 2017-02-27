$(function () {
    function getCookie (name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = $.trim(cookies[i]);
                // Does this cookie begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }

        return cookieValue;
    }

    $(".auth_req").submit(function (event) {
        event.preventDefault();
        var id = $(this).attr("id")
        $.ajax({
            url: $(this).attr("action"),
            method: "POST",
            data: {pk: $(this).attr("id"),
                csrfmiddlewaretoken: getCookie('csrftoken')},
            success: function (response) {
                console.log($("#"+id))
                $("#row-"+id).css("display", "none");
            },
            error: function (res) {
                console.log("FAIL");
                $(this).filter(":input").css('color: blue');
            }
        });
    })
});