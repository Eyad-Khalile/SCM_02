$('body').css('padding-top', $('.navbar').outerHeight() + 'px')

$(".alert").delay(6000).slideUp(1000, function () {
    $(this).alert('close');
});

if ($('nav').length > 0) { // check if element exists
    var last_scroll_top = 0;
    $(window).on('scroll', function () {
        scroll_top = $(this).scrollTop();
        if (scroll_top < last_scroll_top) {
            $('nav').removeClass('scrolled-down').addClass('scrolled-up');
        } else {
            $('nav').removeClass('scrolled-up').addClass('scrolled-down');
        }
        last_scroll_top = scroll_top;
    });
}

