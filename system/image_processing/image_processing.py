import cv2
import os.path
import numpy as np

# Global variables
LOCAL_PATH = os.path.dirname(__file__)  # get current directory


def encode_img_jpg(img):
    return cv2.imencode('.jpg', img)


def yellow_range_color():
    return np.array([20, 100, 100]), np.array([30, 255, 255])


def lane_tracking(image_hsv):
    # define range of color in HSV
    lower_color, upper_color = yellow_range_color()
    # Threshold the HSV image to get only blue colors
    return cv2.inRange(image_hsv, lower_color, upper_color)
