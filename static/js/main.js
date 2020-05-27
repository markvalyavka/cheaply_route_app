$(document).ready(function() {

    var SELECTION = {
        "select_taxi": false,
        "select_cycling": false,
        "select_walking": false,
        "select_car": false,
        "select_transit": false,
    };

    // Car characteristics menu set up 
    $('#driving_btn').click(function() {
        brand_select = $("#car_menu")
        if (brand_select.css("display") == "block") {
            brand_select.css({ "display": "none" })
        } else {
            brand_select.css({ "display": "block" })
        }
    });

    // Submiting data
    $('#submit_data').click(function() {
        if (!$('.address_holder').val() || !$('.destination_holder').val()) {

            $(location).prop('href', "/");
            return;
        };
        $('body').children().css({ "display": "none" })
        $('body').css({ "animation": 'Rainbow 1s' })
        $('body').css({ "animation-iteration-count": "infinite" })

        $('.loading').css({ "display": "block" })

        $('#cloud_1').css({ "animation": 'Cloud1 120s' })
        $('#cloud_1').css({ "animation-iteration-count": "infinite" })

        $('#cloud_2').css({ "animation": 'Cloud2 120s' })
        $('#cloud_2').css({ "animation-iteration-count": "infinite" })

        $('#cloud_3').css({ "animation": 'Cloud3 120s' })
        $('#cloud_3').css({ "animation-iteration-count": "infinite" })
    });

    // Selecting options
    $('.section_btn').click(function() {
        if ($(this).data('type') in SELECTION) {
            if (SELECTION[$(this).data('type')] == true) {
                SELECTION[$(this).data('type')] = false;
                $(this).css({
                    "background-color": "#F7EC91"
                });
            } else {
                SELECTION[$(this).data('type')] = true;
                $(this).css({
                    "background-color": "#D86F6F"
                });
            };
        }
    });

});