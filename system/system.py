import base64
from image_processing.image_processing import *
from camera.camera import Camera
# from picar_v.picar_v import PicarV

# camera = Camera()
# picar_v = PicarV()


# Calling functions to control the robot by image processing
# Return two videos to view: Original and processing videos
def system_main():
    # video1 = camera.get_frame()
    video1 = teste()
    video_processing(video1)


# Video processing
# Return the processing video
# Color image loaded by OpenCV is in BGR mode.
def video_processing(video):

    video_processed = detect_street(video)

    try:
        left_fit, right_fit, video_processed = fit_lines(video_processed)
        left_cur, right_cur, center = curvature(left_fit, right_fit, video_processed)

        add_text_to_image(video_processed, left_cur, right_cur, center)

    except Exception as e:
        print str(e)

    finally:
        show_image(video_processed)


def teste():
    static_path = os.path.join(os.getcwd(), 'images-test/2019-03-25')
    return cv.imread(os.path.join(static_path, 'pista-camera2.jpg'))
