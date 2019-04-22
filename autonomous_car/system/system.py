from constants.constants import FUZZY_CONTROLLER, PROPORCIONAL_CONTROLLER, DETECT_YELLOW, DETECT_BLACK
from image_processing.image_processing import *
from controller.fuzzy_controller import FuzzyController


class System:
    def __init__(self, controller, color_street):
        self._controller = self.__define_controller(controller)
        self._color = color_street

    def output(self, video):
        video_processed, distance_center, curv = self.__video_processing(video)
        speed, angle = self._controller.output(distance_center, curv)
        return video_processed, speed, angle

    # define range of color in HSV
    def __detect_street_by_color(self, video):
        if self._color == DETECT_YELLOW:
            lower_color, upper_color = np.array([20, 0, 100]), np.array([30, 255, 255])
            # lower_color, upper_color = np.array([20, 100, 100]), np.array([30, 255, 255])
        elif self._color == DETECT_BLACK:
            lower_color, upper_color = np.array([0, 0, 0]), np.array([180, 255, 100])
        else:
            raise ValueError('Color to found the street not found!')
        return detect_street(video, lower_color, upper_color)

    # Video processing
    # Return the processing video
    # Color image loaded by OpenCV is in BGR mode.
    def __video_processing(self, video):
        video_street = self.__detect_street_by_color(video)
        try:
            left_fit, right_fit, video_lines = fit_lines(video_street)
            # show_image(video_processed)
            left_cur, right_cur, distance_center = curvature(left_fit, right_fit, video_lines)

            video_road = draw_lines(video, left_fit, right_fit)
            curv = (left_cur + right_cur) / 2
            add_text_to_image(video_road, curv, distance_center)

            return video_road, distance_center, curv

        except Exception as e:
            print str(e)
            return video, 1, 1

    # Define which controller to use
    def __define_controller(controller):
        if controller == FUZZY_CONTROLLER:
            return FuzzyController()
        elif controller == PROPORCIONAL_CONTROLLER:
            print "Proporcional Controller"
        else:
            print "Controller not found"
