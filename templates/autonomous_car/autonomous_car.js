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

function set_turn_left(value){
    return requestHttp("turn_left", value);
}

function set_turn_right(value){
    return requestHttp("turn_right", value);
}

function command_to_car(input){
    var keyChar = String.fromCharCode(input.which);
    switch(keyChar) {
        case 'W':
            set_speed(10);
            run_action('forward');
            break;
        case 'S':
            set_speed(10);
            run_action('backward');
            break;
        case 'O':
            run_action('restart');
            break;
        case 'P':
            run_action('stop');
            break;
        case 'A':
            set_turn_left(45);
            break;
        case 'D':
            set_turn_right(45);
            break;
        default:
            break;
    }
}

get_video_original();

