
// 
$(function() {


  var options;
  var selectMenuBool = true;

    $(".select").selectmenu(); 

    $.ajax({
        url: $("#select-form").attr("action"),
        method: 'GET',
        success: function(resp){
            options = resp;

            console.log($.type(options) === "string");
            if ($.type(options) === "string") {
                return;
            }
            $.each(options, function(key, value){
                console.log("key = " + key);
                $("#select-course").append("<option>" + key + "</option>");
            });

            $.cookie('select_page_to_load', window.location.href);
        }
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

    
    $("#select-course").selectmenu({
            select: function(event, ui) {
               var x = ui.item.label;
               $("#select-semester").find('option').remove().end();
               var option_html = "<option> --- </option>";
               $.each(options[x], function(index, value) {
                    option_html += "<option>" + index + "</option>";
               });
               console.log(option_html);
               $("#select-semester").append(option_html);
               $("#select-semester").selectmenu("refresh");
            }
        });

    /* including this here because several templates have a select-subject div */
    $("#select-semester").selectmenu({
            change: function(event, ui) {
               var x = ui.item.label;
               $("#select-subject").find('option').remove().end();

               var course = $("#select-course :selected").text();

               var option_html = "<option value='0'> --- </option>";

               $.each(options[course][x], function(index, value) {
                    option_html += "<option value="+value[0]+">" + value[1] + "</option>";
               });
               console.log(option_html);
               $("#select-subject").append(option_html);
               $("#select-subject").selectmenu("refresh");

               console.log($("#select-semester :selected"));
               // $("#btn-go").attr("href", $(this + ":selected").val())
            }
       });

    
});
window.addEventListener( "pageshow", function ( event ) {
  var historyTraversal = event.persisted || 
                         ( typeof window.performance != "undefined" && 
                              window.performance.navigation.type === 2 );
  if ( historyTraversal ) {
    // Handle page restore.
    window.location.reload();
  }
});

history.pushState(null, null, '/actions/');