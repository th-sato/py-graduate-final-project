from constants.constants import VIDEO_CAPTURE
from threading import Thread
from system.system import system
from camera.camera import Camera
# from picar_v.picar_v import PicarV
import os
import cv2 as cv


class AutonomousCar:
    def __init__(self, controller):
        self._stop_car = False
        self._controller = controller
        self._video_processed = None
        self._video_original = None
        # self.picar_v = PicarV()
        self._camera = Camera(VIDEO_CAPTURE)
        self._camera.start()

    def start(self):
        Thread(target=self.update, args=()).start()

    def restart(self):
        self._stop_car = False
        self._camera.restart()
        self.start()

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
        while not self._stop_car:
            self._video_original = self.image_test()
            # self._video_original = self._camera.frame
            self._video_processed, speed, angle = system(self._video_original, self._controller)
            # self.picar_v.speed(speed)
            # self.picar_v.turn(angle)

    def image_test(self):
        static_path = os.path.join(os.getcwd(), 'images-test/2019-03-25')
        return cv.imread(os.path.join(static_path, 'pista-camera2.jpg'))
