$(function () {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    var saveform = $("#save-form");

    var post_data = {}

    saveform.submit(function(event) {
        event.preventDefault();

        users = $(".student-name").each(function(index){
            var name = $(this).find("span");
            post_data[name.html()] = {};

            var att_array = {};
            $("input[name="+ name.html() +"]").each(function(index) {
                //console.log($(this).attr("name") + ":" + $(this).is(":checked"));
                var id = $(this).prev("span").html();
                console.log(id);
                att_array[id] = $(this).is(":checked");
            })
            post_data[name.html()] = att_array;
        });
        
        console.log(post_data);
        
        // Perhaps using JSON here is a better idea but CSRF validation doesn't
        // work with JSON. So that may be changed in the future but as of now this
        // works.
        post_data['csrfmiddlewaretoken'] = csrftoken;
        $.ajax({
            url: saveform.attr('action'),
            data: post_data,
            method: "POST",
            success: function() {
                console.log('yay');
            },
        });
    });

});