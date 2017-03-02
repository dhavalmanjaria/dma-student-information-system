
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
        if ($(this).val() == "a.m.") {
            $(this).val('p.m.');
            $(this).next(".hidden-a").val('p.m.');
        }
        else {
            $(this).val('a.m.');
            $(this).next().val('a');
            $(this).next(".hidden-a").val('a.m.');
        }
        event.preventDefault();
    });
});