from constants.constants import VIDEO_CAPTURE, URL_REDIS_IMAGE, KEY_JSON_IMAGE
from threading import Thread
import requests
import time
from system.system import System
from system.image_processing.image_processing import jpgimg_to_base64
from picar_v.camera.camera import Camera
from picar_v.robot import Robot
# import os
# import cv2 as cv


class AutonomousCar:
    def __init__(self, controller, color_street):
        self._stop_car = False
        self._controller = controller
        self._color_street = color_street
        self._video_processed = None
        self._video_original = None
        self._robot = Robot()
        self._camera = Camera(VIDEO_CAPTURE)
        self._camera.start()

    def __start(self):
        Thread(target=self.update, args=()).start()

    def start(self):
        self._stop_car = False
        self._camera.start()
        self.__start()

    def stop(self):
        self._stop_car = True
        self._camera.stop()
        time.sleep(2)
        self._robot.stop_car()

    @property
    def video_original(self):
        return self._video_original

    @property
    def video_processed(self):
        return self._video_processed

    @staticmethod
    def request_post_image(url, key_img, img):
        requests.post(url, json={key_img: img})

    def backwheel_calib(self, action):
        self._robot.calibration_back_wheel(action)

    def frontwheel_calib(self, action):
        self._robot.calibration_front_wheel(action)

    def commands_by_request(self, command):
        if command == "forward":
            self._robot.speed(40)
            self._robot.forward()
        elif command == "backward":
            self._robot.speed(40)
            self._robot.backward()
        elif command == "right":
            self._robot.turn(35)
        elif command == "left":
            self._robot.turn(-35)
        elif command == "straight":
            self._robot.turn(0)
        elif command == "stop":
            self._robot.stop_car()
        else:
            print "Command to Picar-V not found"

    def update(self):
        system = System(self._controller, self._color_street)
        while not self._stop_car:
            # self._video_original = self.image_test()
            self._video_original = self._camera.frame
            self._video_processed, speed, angle = system.output(self._video_original)
            self.request_post_image(URL_REDIS_IMAGE, KEY_JSON_IMAGE, jpgimg_to_base64(self._video_processed))
            self._robot.speed(speed)
            self._robot.turn(angle)

    # @staticmethod
    # def image_test():
    #     static_path = os.path.join(os.getcwd(), '../images-test/2019-03-25')
    #     return cv.imread(os.path.join(static_path, 'pista-camera1.jpg'))
