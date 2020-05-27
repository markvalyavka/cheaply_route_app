$(document).ready(function () {

    unwrapCardData()
    // Unwrapping cards into carousel
    function unwrapCardData() {
        var card_width = getCardWidth();
        var per_slide = Math.floor(12 / card_width)
        $('#menu_carousel_inner').append('<div class="carousel-item active" style="min-height:400px;"><div class="row"></div></div>')
        var i = 0;
        $('#data_wrapper').children('.card_item').each(function () {
            if(i === per_slide){
                $('#menu_carousel_inner').append('<div class="carousel-item" style="min-height:400px;"><div class="row"></div></div>')
                i = 0;
            };
            slide = $('.carousel-item').last()
            slide = slide.children().first()
            slide.append(this);
            $(this).addClass(`col-lg-${card_width} col-md-${card_width} col-${card_width}`);
            i++;
        });

    }

    // Getting card width based on screen size
    function getCardWidth() {
        var scr_width = $(window).width();
        if (scr_width <= 768) {
            return 12
        }
        if (768 < scr_width && scr_width <= 992) {
            return 6
        }
        if (992 < scr_width) {
            return 4
        }
    }
});