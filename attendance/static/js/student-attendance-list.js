$(function() {
    $("#select-month").selectmenu(
        "option", "select", function(){
            var month = $("#select-month option:selected").val();
            idx =  window.location.href.lastIndexOf('?');
            if (idx === "-1")
                idx = window.location.href.length + 1;
            url = window.location.href.slice(0, idx);
            $("#btn-go").attr("href", url + "?month=" + month)
        }
    );
});