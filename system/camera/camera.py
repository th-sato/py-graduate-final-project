import cv2 as cv


class Camera:
    def __init__(self):
        self.video = cv.VideoCapture(0)
        _, self.frame = self.video.read()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        _, self.frame = self.video.read()
        return self.frame
