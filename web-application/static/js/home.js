var interval = 1;
var HOST_REDIS_IMAGE = 'http://localhost:8081/redis-image'
var HOST_AUTONOMOUS_CAR = 'http://192.168.1.234:5000';
//var HOST_AUTONOMOUS_CAR = 'http://localhost:8081';

function get_video_original() {
    $.ajax({
        type: 'GET',
        url: HOST_REDIS_IMAGE,
//        xhrFields: {
//           withCredentials: true
//        },
//        crossDomain: true,
        success: function (res) {
            $("#video_processed").attr("src", res);
            setTimeout(get_video_original, interval);
        },
    });
}

function requestGetHttp(path){
    var xmlHttp   = new XMLHttpRequest();
    url = HOST_AUTONOMOUS_CAR + "/" + path;
    xmlHttp.open("GET", url, true);
    xmlHttp.send(null);
    return xmlHttp.responseText;

}

function requestPostHttp(path, json){
    var xmlHttp   = new XMLHttpRequest();
    var protocol  = window.location.protocol;
    url = HOST_AUTONOMOUS_CAR + "/" + path;
    xmlHttp.open("POST", url, true);
    xmlHttp.setRequestHeader("Content-Type", "application/json");
    xmlHttp.send(json);
    return xmlHttp.responseText;
}

function start_autonomous_car() {
    requestGetHttp('start')
}

function stop_autonomous_car() {
    requestGetHttp('stop')
}

function calibration(wheel, command) {
    json = JSON.stringify({ "wheel": wheel, "action": command })
    requestPostHttp("commands-by-request", json)
}

function commands_to_car(command) {
    json = JSON.stringify({ "command": command })
    requestPostHttp("calibration", json)
}

get_video_original()