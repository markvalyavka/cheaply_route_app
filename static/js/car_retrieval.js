let brand_id = 0
var cors_api_url = 'https://cors-anywhere.herokuapp.com/';
CAR_ID = ''

function doCORSRequest(options, printResult) {
    var x = new XMLHttpRequest();
    x.open(options.method, cors_api_url + options.url);
    x.onload = x.onerror = function() {
        printResult(
            options.method + ' ' + options.url + '\n' +
            x.status + ' ' + x.statusText + '\n\n' +
            (x.responseText || '')
        );
    };
    x.send(options.data);
}

function selectBrand(obj) {
    brand_id = obj.value
    if ($('#select_model').length) { $('#select_model').remove() }
    if ($('#input_spec').length) { $('#input_spec').remove() }
    $('.select_model').append(`<select class='section_btn' onchange='selectModel(this)' id='select_model' style='margin:20px;' ></select>`)
    let outputField = $('#select_model')
    displayLoading(true)
    doCORSRequest({
        method: 'GET',
        url: `http://autoportal.ua/compare_model.html?brand_id=${brand_id}&catalog_id=1&cg_id=`,
        data: ''
    }, function printResult(result) {
        let parser = new DOMParser();
        result = parser.parseFromString(result, "text/html");
        option_list = $(result).find('option');

        for (let i = 0; i < option_list.length; i++) {
            outputField.append(option_list[i]);
        };
        $("#select_model").val($("#select_model option:first").val());
        setTimeout(displayLoading(false), 7000);
    });
}

function displayLoading(start) {
    if (start) {
        $('#car_menu').css({ "animation": 'Rainbow 0.5s' })
        $('#car_menu').css({ "animation-iteration-count": "infinite" })
        $('#car_menu').children().css({ "display": "none" })
    } else {
        $('#car_menu').css({ "animation": 'none' })
        $('#car_menu').children().css({ "display": "flex" })
    }
}

function selectModel(obj) {
    if ($('#input_spec').length) { $('#input_spec').remove() }
    $('.select_spec').append('<label for="select_spec"></label>')
    $('.select_spec').append('<input id="input_spec" type="text" name="spec_list" list="spec_list" class="section_btn mx-auto d-block" style="margin-top:0px; margin-bottom:20px;">')
    $('.select_spec').append(`<datalist id='spec_list'></datalist>`)
    let outputField = $('#spec_list')
    displayLoading(true)
    doCORSRequest({
        method: 'GET',
        url: `http://autoportal.ua/compare_model.html?brand_id=${brand_id}&catalog_id=1&cg_id=${obj.value}`,
        data: ''
    }, function printResult(result) {
        let parser = new DOMParser();
        result = parser.parseFromString(result, "text/html");
        option_list = $(result).find('option')
        for (let i = 0; i < option_list.length; i++) {
            outputField.append(option_list[i]);
        }
        setTimeout(displayLoading(false), 7000);
    });
}