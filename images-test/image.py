import os
import cv2 as cv
import numpy as np


def show_image(img):
    cv.imshow('image', img)
    # cv.waitKey(10)
    cv.waitKey(0)
    # cv.destroyAllWindows()


# img_binary contains only 0 or 255
def detect_street(img, lower_color, upper_color):
    img_hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    # interval = img.shape[0] / 2, int(img.shape[0] * (1.0 - 1.0 / 8.0))
    # img_hsv = img_hsv[interval[0]:interval[1], :]
    # Threshold the HSV image to get only the selected colors
    img_processed = cv.inRange(img_hsv, lower_color, upper_color)
    img_processed[img_processed == 255] = 120
    return img_processed


def image_test():
    static_path = os.path.join(os.getcwd(), '2019-04-20')
    return cv.imread(os.path.join(static_path, 'black-road.jpg'))


if __name__ == "__main__":
    lower_color, upper_color = np.array([0, 0, 0]), np.array([180, 255, 50])
    img = detect_street(image_test(), lower_color, upper_color)
    show_image(img)