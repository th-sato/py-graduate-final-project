import base64
from camera.camera import Camera
from controller.controller import controller
from image_processing.image_processing import *


# Calling functions to control the robot by image processing
# Return two videos to view: Original and processing videos
def system_main():
    # Get video
    # video1 = Camera().get_frame()
    video1 = teste()
    # Processing video
    video2 = video_processing(video1)
    # Action PiCar-V (controller send commands to Picar-V)s
    return return_videos(video1, video2)


# Video processing
# Return the processing video
# Color image loaded by OpenCV is in BGR mode.
def video_processing(video):
    video_hsv = cv.cvtColor(video, cv.COLOR_BGR2HSV)
    # return lane_tracking(video_hsv)
    # return lane_detector(video_hsv)
    _, img_bin = lane_detector(video_hsv)
    teste = fit_lines(img_bin)
    return img_bin


def return_videos(video_original, video_processed):
    return {"video_original": show_html(video_original), "video_processed": show_html(video_processed)}


def show_html(img):
    ret, jpg = encode_img_jpg(img)
    return base64.b64encode(jpg)


def teste():
    static_path = os.path.join(os.getcwd(), 'static/images')
    return cv.imread(os.path.join(static_path, 'pista-camera.jpg'))
