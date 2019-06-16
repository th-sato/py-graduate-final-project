//var interval = 1;
//var HOST = 'http://localhost:8081';
//var HOST_REDIS_IMAGE = 'http://localhost:8081/redis-image'
//var HOST_AUTONOMOUS_CAR = 'http://192.168.1.234:5000';

//function get_video_original() {
//    $.ajax({
//        type: 'GET',
//        url: HOST + '/redis-image',
////        xhrFields: {
////           withCredentials: true
////        },
////        crossDomain: true,
//        success: function (res) {
//            $("#video_processed").attr("src", res);
//            setTimeout(get_video_original, interval);
//        },
//    });
//}

var HTML_IMAGE_HEADER = "data:image/png;base64, ";


function requestGetHttp(path, is_asynchronous){
    var xmlHttp   = new XMLHttpRequest();
//    url = HOST + "/" + path;
    url = "/" + path;
    xmlHttp.open("GET", url, is_asynchronous);
    xmlHttp.send(null);
    return xmlHttp.responseText;
}

function requestPostHttp(path, json){
    var xmlHttp   = new XMLHttpRequest();
    var protocol  = window.location.protocol;
//    url = HOST + "/" + path;
    url = "/" + path;
    xmlHttp.open("POST", url, true);
    xmlHttp.setRequestHeader("Content-Type", "application/json");
    xmlHttp.send(json);
    return xmlHttp.responseText;
}

function start_autonomous_car() {
    requestGetHttp('start', true)
}

function stop_autonomous_car() {
    requestGetHttp('stop', true)
}

function calibration(wheel, command) {
    json = JSON.stringify({ "wheel": wheel, "action": command })
    requestPostHttp("calibration", json)
}

function commands_to_car(command) {
    json = JSON.stringify({ "command": command })
    requestPostHttp("commands-by-request", json)
}

function speed_wheel_car() {
    speed = document.getElementById("speed-input").value
    angle = document.getElementById("angle-input").value
    json = JSON.stringify({ "speed": speed, "angle": angle })
    requestPostHttp("input-values", json)
}


function find_first_element_true(element_name, n) {
    for(let i = 0; i < n; i++) {
        let option = element_name + "[" + i + "]";
        if (document.getElementById(option).checked) {
            return document.getElementById(option).value
        }
    }
}

function change_option_video() {
    qtd_option = 2
    video_prefix = "video"
    selected_video = find_first_element_true(video_prefix, qtd_option)
    json = JSON.stringify({ "selected_video": selected_video })
    requestPostHttp("selected-video", json)
}

function update_video() {
    document.getElementById("my-video").load();
}

function img_processed_camera() {
    path = "get-image-processed-camera"
    res = JSON.parse(requestGetHttp(path, false))
    document.getElementById("img_camera").src = HTML_IMAGE_HEADER + res["img"]
}

function img_original_camera() {
    path = "get-image-original-camera"
    res = JSON.parse(requestGetHttp(path, false))
    document.getElementById("img_camera").src = HTML_IMAGE_HEADER + res["img"]
}

function activate_controller(activate) {
    path = "controller-active"
    json = JSON.stringify({ "active": activate })
    requestPostHttp(path, json)
}

function update_graphics(){
    qtd_images = 4
    path_update_images = 'update-graphics'
    requestGetHttp(path_update_images, false)

    path_get_images = 'get-img-by-id?img_id='
    for(let i = 0; i < qtd_images; i++) {
        path_img = path_get_images + i
        resp = JSON.parse(requestGetHttp(path_img, false))
        element_id = 'graphics[' + i + ']'
        document.getElementById(element_id).src = HTML_IMAGE_HEADER + resp["img"]
    }

}


window.onload = function() {
    update_graphics();
};
