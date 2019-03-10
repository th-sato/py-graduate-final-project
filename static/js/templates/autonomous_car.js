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

get_video_original()
