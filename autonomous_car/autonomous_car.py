from constants.constants import VIDEO_CAPTURE, URL_BACK
from threading import Thread
import requests
from system.system import System
from system.image_processing.image_processing import jpgimg_to_base64
from picar_v.camera.camera import Camera
# from picar_v.robot import Robot
import os
import cv2 as cv


class AutonomousCar:
    def __init__(self, controller):
        self._stop_car = False
        self._controller = controller
        self._video_processed = None
        self._video_original = None
        # self.robot = Robot()
        self._camera = Camera(VIDEO_CAPTURE)
        self._camera.start()

    def __start(self):
        Thread(target=self.update, args=()).start()

    def start(self):
        self._stop_car = False
        self._camera.start()
        self.__start()

    def stop(self):
        self._camera.stop()
        self._stop_car = True

    @property
    def video_original(self):
        return self._video_original

    @property
    def video_processed(self):
        return self._video_processed

    def update(self):
        system = System(self._controller)
        while not self._stop_car:
            # self._video_original = self.image_test()
            self._video_original = self._camera.frame
            self._video_processed, speed, angle = system.output(self._video_original)

            requests.post(URL_BACK, json={"IMG", jpgimg_to_base64(self._video_processed)})
            # self.robot.speed(speed)
            # self.robot.turn(angle)

    @staticmethod
    def image_test():
        static_path = os.path.join(os.getcwd(), '../images-test/2019-03-25')
        return cv.imread(os.path.join(static_path, 'pista-camera1.jpg'))