var interval = 1;

function get_video_original() {
    $.ajax({
        type: 'GET',
        url: 'http://localhost:8081/redis-image',
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

get_video_original()