$('body').css('padding-top', $('.navbar').outerHeight() + 'px')

$('#navbarSupportedContent').find('.nav-link').css('height', $('.navbar').outerHeight() + 'px');

// AOS.init();

// $('#sidebar-wrapper').css('height', $('#sidebar-wrapper').parent().parent('div.col-2').outerHeight() + 'px');
// $('#sidebar-wrapper').css('height', $('div.min-vh-100').outerHeight() + 'px');

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
let width_col = $('.col-2.min-vh-100').outerWidth();
// $('#sidebar-wrapper').css('width', width_col);

$('#menu-toggle').click(function (e) {
    e.preventDefault();

    // $('#sidebar-wrapper').css('width', '50px');
    $('#wrapper').toggleClass('menuDisplayed', 7000, "easeInQuad");
    $('.sidebar-navbar').find('a').toggleClass('d-none', 7000, "easeOutSine");

    // $('.fa-tachometer-alt').toggleClass('d-none');

    // $('.nav-link').toggleClass('d-none');

    $('#menu-toggle svg').toggleClass('fa-angle-double-right fa-angle-double-left');
    // $('i.fa')

    $('#wrapper').parent().toggleClass('col-2');
    $('#wrapper').parent().toggleClass('min-vh-100');
    $('#wrapper').parent().next().toggleClass('col-10 col-12');

});


// SLIDER HEIGHT
let nav_height = $('.navbar').outerHeight();
let screen_height = $(window).height();






// SLIDER
// $('.skitter-large').skitter();
// $('.slider').bxSlider();


// $('#org_lider').slick({
//     autoplay: true,
// });


// URL
var pathname = window.location.pathname; // Returns path only (/path/example.html)

if (pathname == '/' || pathname == 'en') {
    $('#sider_bg').css('height', screen_height + 'px');
}

$('#wrapper').css('height', nav_height + 'px');


// GET THE SELECTED FILE NAME
$('#id_logo').change(function(e){
    var fileName = e.target.files[0].name;
    $('.logo_file_name').html('The logo "' + fileName + '" has been selected.');
});


// SLIDE HOME PAGE 
$('#carouselHomePage').css('height', screen_height + 'px !important');
$('#carouselHomePage').find('img').css('height', screen_height + 'px !important');

// console.log($('#carouselHomePage').height());
// console.log($('#carouselHomePage').find('img').height());


$('#carouselHomePage').carousel({
    pause: false,
    interval: 4000,
});



// FUNCTION FOR THE SCROLL 
$(window).scroll(function () {
    
    // NAVBAR
    if ($(document).scrollTop() > ($(window).height() - 50)) {
        $('nav').addClass('nav-bg-scroll');
    }
    else {
        $('nav').removeClass('nav-bg-scroll');
    }

    // BTN TOP
    if ($(document).scrollTop() > ($(window).height() - 500)) {
        $('#f-5-top').fadeOut(1500).removeClass('d-none').fadeIn(1500);
    }
    else {
        $('#f-5-top').fadeIn(1500).addClass('d-none').fadeOut(1500);
    }
    
});




$('#carouselOrgs').carousel({
    pause: false,
    interval: 4000,
    // prev: false,
    // next: false,
});

$('#carouselOrgs').carousel({
    pause: false,
    interval: 60000,
});

// SCROLL TOP 
$("#scroll_top").click(function() {
  $("html, body").animate({ scrollTop: 0 }, "slow");
  return false;
});

let i = 0;
$('#sidebar-wrapper').find('.btn-down').each(function () {
    $(this).on('click', function () {
        i++;
        let m_t = $('#sidebar-wrapper').find('ul.sidebar-navbar').css('margin-top');
        if (m_t != '-240px') {
            $('#sidebar-wrapper').find('ul.sidebar-navbar').css({'margin-top': '-'+i+'rem'}, "slow");
        }
    });    
});


$('#sidebar-wrapper').find('.btn-up').each(function () {
    $(this).on('click', function () {
        i++;
        let m_t = $('#sidebar-wrapper').find('ul.sidebar-navbar').css('margin-top');
        if (m_t < 0) {
            $('#sidebar-wrapper').find('ul.sidebar-navbar').css({'margin-top': i+'rem'}, "slow");
        } else {
            $('#sidebar-wrapper').find('ul.sidebar-navbar').css({'margin-top':'0'}, "slow");
        }
    });    
});

