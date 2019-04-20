from threading import Thread
import cv2 as cv


class Camera:
    def __init__(self, source=0):
        self._video = cv.VideoCapture(source)
        self._video.set(cv.CAP_PROP_FRAME_WIDTH, 432.)
        self._video.set(cv.CAP_PROP_FRAME_HEIGHT, 240.)
        _, self._frame = self._video.read()
        self._stop = False

        # self.video.set(cv.cv.CV_CAP_PROP_FRAME_WIDTH, 432.)
        # self.video.set(cv.cv.CV_CAP_PROP_FRAME_HEIGHT, 240.)
        # self.video.set(cv.cv.CV_CAP_PROP_FRAME_WIDTH, 1920.)
        # self.video.set(cv.cv.CV_CAP_PROP_FRAME_HEIGHT, 1200.)

    def __del__(self):
        self._video.release()

    def __start(self):
        Thread(target=self.update, args=()).start()

    def start(self):
        self._stop = False
        self.__start()

    def update(self):
        while not self.stop:
            _, self.frame = self.video.read()

    def stop(self):
        self._stop = True

    @property
    def frame(self):
        return self._frame

