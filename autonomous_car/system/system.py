from constants.constants import FUZZY_CONTROLLER, PROPORCIONAL_CONTROLLER
from image_processing.image_processing import *
from controller.fuzzy_controller import FuzzyController

fuzzy_controller = FuzzyController()


def system(video, controller):
    video_processed, center, curv = video_processing(video)
    speed, angle = control(controller, center, curv)
    return video_processed, speed, angle


# Video processing
# Return the processing video
# Color image loaded by OpenCV is in BGR mode.
def video_processing(video):
    video_street = detect_street(video)

    try:
        a = 1
        # left_fit, right_fit, video_processed = fit_lines(video_street)
        # left_cur, right_cur, center = curvature(left_fit, right_fit, video_processed)
        #
        # curv = (left_cur + right_cur) / 2
        # add_text_to_image(video_processed, curv, center)
        # # draw_lines()

    except Exception as e:
        print str(e)

    finally:
        return video_street, 1, 1
        # return video_processed, center, curv


# Define which controller to use
# Return speed, angle
def control(controller, center, curv):
    if controller == FUZZY_CONTROLLER:
        fuzzy_controller.teste()

    elif controller == PROPORCIONAL_CONTROLLER:
        print "Controller"

    else:
        print "Controller not found"

    return 1, 2