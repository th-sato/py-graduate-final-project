import base64
from image_processing.image_processing import *
from camera.camera import Camera
import constants.constants as const
# from picar_v.picar_v import PicarV

camera = Camera()
# picar_v = PicarV()


# Calling functions to control the robot by image processing
# Return two videos to view: Original and processing videos
def system_main():
    video1 = camera.get_frame()
    # video1 = teste()
    video2 = video_processing(video1)
    return return_videos(video1, video2)


# Video processing
# Return the processing video
# Color image loaded by OpenCV is in BGR mode.
def video_processing(video):
    video_hsv = cv.cvtColor(video, cv.COLOR_BGR2HSV)

    video_processed = detect_yellow_street(video_hsv)

    try:
        left_fit, right_fit, video_processed = fit_lines(video_processed)
        left_cur, right_cur, center = curvature(left_fit, right_fit, video_processed)

        add_text_to_image(video_processed, left_cur, right_cur, center)

    except Exception as e:
        print str(e)

    finally:
        return video_processed


def return_video(video_original):
    return const.HTML_IMAGE_HEADER + show_html(video_original)


def return_videos(video_original, video_processed):
    return {"video_original": return_video(video_original), "video_processed": return_video(video_processed)}


def show_html(img):
    ret, jpg = encode_img_jpg(img)
    return base64.b64encode(jpg)


def teste():
    static_path = os.path.join(os.getcwd(), 'static/images')
    return cv.imread(os.path.join(static_path, 'pista-camera2.jpg'))
