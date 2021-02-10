// Sticky header with jQuery
$(window).bind('scroll', function () {
    var scroll = $(window).scrollTop();
    if (scroll > 90){
        $('#myHeader').addClass('sticky');
    } else {
        $('#myHeader').removeClass('sticky');
    }
});