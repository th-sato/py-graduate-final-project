from image_processing.image_processing import *
from controller.fuzzy_controller import FuzzyController
from controller.pid_controller import PIDController
from logs.log_dto import LogDto
from logs.log import Log
import time


class System:
    def __init__(self, controller, color_street):
        self._controller = self.__define_controller(controller)
        self._color = color_street
        self._log = Log()
        self._initial_time = time.time()

    def output(self, video, img_to_show):
        video_processed, dist_center, curv = self.__video_processing(video)
        curv_max = self.__set_max(curv, -200.0, 200.0)
        dist_center_max = self.__set_max(dist_center, -0.5, 0.5)
        run_time = self.__get_run_time()
        speed, angle = self._controller.output(dist_center_max, curv_max, run_time)
        # self.__store_object_log(speed, angle, dist_center, curv)
        self.__store_object_log(speed, angle, dist_center_max, curv_max, run_time)

        if img_to_show == STREET_ORIGINAL_IMAGE:
            return video, speed, angle
        # elif img_to_show == STREET_DETECTING:
        #     return self.__detect_street_by_color(video), speed, angle
        elif img_to_show == STREET_LINES_DRAWN:
            return video_processed, speed, angle
        else:
            print "img_to_show: ", img_to_show, " not found!"
            return video, 0, 0

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
            left_fit, right_fit, video_shape = fit_lines(video_street)
            # show_image(video_processed)
            left_cur, right_cur, left_x, right_x, distance_center = curvature(left_fit, right_fit, video_shape)

            video_road = draw_lines(video, left_x, right_x)
            curv = (left_cur + right_cur) / 2.0
            add_text_to_image(video_road, curv, distance_center)

            return video_road, distance_center, curv

        except Exception as e:
            print str(e)
            return video, 0, 0

    def reset_log(self):
        self._log.clean_log()
        self._initial_time = time.time()
        self._controller.reset(self._initial_time)

    def get_log_system(self):
        return self._log.get_log()

    def __store_object_log(self, speed, angle, dist_center, curv, run_time):
        try:
            log_object = LogDto(run_time, speed, angle, dist_center, curv)
            log_obj_str = repr(log_object)
            self._log.store_object(log_obj_str)
        except Exception as e:
            print "Error while storing log: ", str(e)

    def __get_run_time(self):
        return time.time() - self._initial_time

    # Define which controller to use
    @staticmethod
    def __define_controller(controller):
        if controller == FUZZY_CONTROLLER:
            return FuzzyController()
        elif controller == PID_CONTROLLER:
            return PIDController()
        else:
            print "Controller not found"

    @staticmethod
    def __set_max(value, min_value, max_value):
        if value > 0 and value > max_value:
            return max_value
        if value < 0 and value < min_value:
            return min_value
        return value
