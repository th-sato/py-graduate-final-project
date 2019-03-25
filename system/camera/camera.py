import cv2 as cv


class Camera:
    def __init__(self):
        self.video = cv.VideoCapture(0)
        self.video.set(cv.cv.CV_CAP_PROP_FRAME_WIDTH, 432.)
	self.video.set(cv.cv.CV_CAP_PROP_FRAME_HEIGHT, 240.)
#	self.video.set(cv.cv.CV_CAP_PROP_FRAME_WIDTH, 432.)
#	self.video.set(cv.cv.CV_CAP_PROP_FRAME_HEIGHT, 240.)
#       self.video.set(cv.cv.CV_CAP_PROP_FRAME_WIDTH, 1920.)
#       self.video.set(cv.cv.CV_CAP_PROP_FRAME_HEIGHT, 1200.)
        _, self.frame = self.video.read()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        _, self.frame = self.video.read()
        return self.frame
