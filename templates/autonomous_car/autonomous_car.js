var interval = 1;

function get_video_original() {
    $.ajax({
        type: 'GET',
        url: '/images',
        success: function (res) {
            $("#video_original").attr("src", res.video_original);
            $("#video_processed").attr("src", res.video_processed);
            setTimeout(get_video_original, interval);
        },
    });
}

function requestHttp(name, value){
    var xmlHttp   = new XMLHttpRequest();
    var protocol  = window.location.protocol;
    var host      = window.location.host;
    var pathname  = "/commands_by_request/";
    url = protocol + "//" + host + pathname + "?" + name + "=" + value;
    console.log(url);
    xmlHttp.open("GET", url, false);
    xmlHttp.send(null);
    return xmlHttp.responseText;
}

function run_action(value){
    return requestHttp("action", value);
}

function set_speed(value){
    return requestHttp("speed", value);
}

function set_turn(value){
    return requestHttp("turn", value);
}

function calibration_back_wheel(wheel) {
    return requestHttp("cali_wheel", wheel);
}

function command_to_car(input){
    var keyChar = String.fromCharCode(input.which);
    switch(keyChar) {
        case 'W':
            run_action('forward');
            set_speed(10);
            break;
        case 'S':
            run_action('backward');
            set_speed(10);
            break;
        case 'A': //Left
            set_turn(-45);
            break;
        case 'D': //Right
            set_turn(45);
            break;
        case 'O':
            run_action('restart');
            break;
        case 'P':
            run_action('stop');
            break;
        case 'L':
            calibration_back_wheel('left');
            break;
        case 'Ç':
            calibration_back_wheel('right');
            break;
        default:
            break;
    }
}

get_video_original();

