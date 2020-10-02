$('body').css('padding-top', $('.navbar').outerHeight() + 'px')

// $('#sidebar-wrapper').css('height', $('#sidebar-wrapper').parent().parent('div.col-2').outerHeight() + 'px');
$('#sidebar-wrapper').css('height', $('div.main-content').outerHeight() + 'px');

$(".alert").delay(6000).slideUp(1000, function () {
    $(this).alert('close');
});

// NAVBAR ANIMATIONS
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


// URL
// var pathname = window.location.pathname;
// if (pathname == "/profile_supper/" || pathname == "/en/profile_supper/") {
//     $('div.main-container').removeClass('container').addClass('container-fluid');
// }

// TOGEL CLASS SHOW FROM THE COLLEPAS
$('a[data-toggle="collapse"]').on('click', function () {
    $('div.collapse.show').removeClass('show');
    $(this).addClass('show');
});

// DASHBOARD SIDEBAR
$('#menu-toggle').click(function (e) {
    e.preventDefault();

    $('#wrapper').toggleClass('menuDisplayed', 7000, "easeInQuad");
    $('.sidebar-navbar').toggleClass('d-none', 7000, "easeOutSine");

    $('i.fa').toggleClass('fa-angle-double-right fa-angle-double-left');

    $('#wrapper').parent().toggleClass('col-2');
    $('#wrapper').parent().toggleClass('min-vh-100');
    $('#wrapper').parent().next().toggleClass('col-10 col-12');



});