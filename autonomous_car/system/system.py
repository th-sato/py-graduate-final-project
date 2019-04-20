from constants.constants import FUZZY_CONTROLLER, PROPORCIONAL_CONTROLLER
from image_processing.image_processing import *
from controller.fuzzy_controller import FuzzyController


class System:
    def __init__(self, controller):
        self._controller = controller

    def output(self, video):
        video_processed, center, curv = self.video_processing(video)
        # show_image(video_processed)
        speed, angle = self.control(center, curv)
        return video_processed, speed, angle

    # Video processing
    # Return the processing video
    # Color image loaded by OpenCV is in BGR mode.
    @staticmethod
    def video_processing(video):
        video_street = detect_street(video)
        try:
            left_fit, right_fit, video_processed = fit_lines(video_street)
            # show_image(video_processed)
            left_cur, right_cur, center = curvature(left_fit, right_fit, video_processed)

            curv = (left_cur + right_cur) / 2
            add_text_to_image(video_processed, curv, center)
            video_processed = draw_lines(video, left_fit, right_fit)

        except Exception as e:
            print str(e)

        finally:
            return video_processed, 1, 1
            # return video_processed, center, curv

    # Define which controller to use
    # Return speed, angle
    def control(self, center, curv):
        if self._controller == FUZZY_CONTROLLER:
            FuzzyController.teste()

        elif self._controller == PROPORCIONAL_CONTROLLER:
            print "Controller"

        else:
            print "Controller not found"

        return 1, 2
