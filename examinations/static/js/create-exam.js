$(function () {
    var getYear = function() {
        var year = $(".next-year").prev(".academic_year").val();
        console.log(year);
        /* This condition is for the view-exams page */
        if (isNaN(year) || year === "" || year === null){
            year = $(".next-year").prev(".academic_year").html();
        }
        year = year.slice(2);
        year = parseInt(year);
        year += 1;
        $(".next-year").html("'" + year);
    }

    getYear();

    $(".next-year").prev(".academic_year").change(getYear);
    
})