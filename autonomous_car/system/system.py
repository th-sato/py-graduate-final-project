from image_processing.image_processing import *
from controller.fuzzy_controller import FuzzyController
from logs.log_dto import LogDto
from logs.log import Log


class System:
    def __init__(self, controller, color_street):
        self._controller = self.__define_controller(controller)
        self._color = color_street
        self._log = Log()

    def output(self, video, img_to_show):
        video_processed, dist_center, curv = self.__video_processing(video)
        curv_max = self.__set_max(curv, 200.0)
        dist_center_max = self.__set_max(dist_center, 0.5)
        speed, angle = self._controller.output(dist_center_max, curv_max)
        self.__store_object_log(speed, angle, dist_center, curv)

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

    def get_log_system(self):
        return self._log.get_log()

    def __store_object_log(self, speed, angle, dist_center, curv):
        try:
            log_object = LogDto()
            log_object.speed = speed
            log_object.angle = angle
            log_object.dist_center = dist_center
            log_object.curv = curv
            self._log.store_object(log_object)
        except Exception as e:
            print "Error while storing log: ", str(e)

    # Define which controller to use
    @staticmethod
    def __define_controller(controller):
        if controller == FUZZY_CONTROLLER:
            return FuzzyController()
        elif controller == PROPORCIONAL_CONTROLLER:
            print "Proporcional Controller"
        else:
            print "Controller not found"

    @staticmethod
    def __set_max(value, max):
        if value > max:
            return max
        return value
