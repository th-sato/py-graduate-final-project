import cv2 as cv
import os.path
import numpy as np
import system.constants.constants as Constants

# Global variables
LOCAL_PATH = os.path.dirname(__file__)  # get current directory


def encode_img_jpg(img):
    return cv.imencode('.jpg', img)


def add_text_to_image(img, left_cur, right_cur, center):
    cur = (left_cur + right_cur)/2.

    font = cv.FONT_HERSHEY_SIMPLEX
    cv.putText(img, 'Radius of Curvature = %d(m)' % cur, (50, 50), font, 0.7, (255, 255, 255), 1)

    left_or_right = "left" if center < 0 else "right"
    cv.putText(img, 'Vehicle is %.2fcm %s of center' % (np.abs(center), left_or_right), (50, 100), font, 0.7,
                (255, 255, 255), 1)


# img_binary contains only 0 or 255
def threshold_yellow_street(img_hsv):
    yellow_range = np.array([20, 100, 100]), np.array([30, 255, 255])
    # define range of color (yellow) in HSV
    lower_color, upper_color = yellow_range
    # Threshold the HSV image to get only the selected colors
    img_lane = cv.inRange(img_hsv, lower_color, upper_color)
    return img_lane


# Alterar
# Considerar os seguintes casos:
# 1) Parar a execucao ao encontrar o primeiro 255.
#       a) Do 0 ate o fim
#       b) Do fim ate o zero
# 2) E se houver somente um dos lados da pista na imagem?
# 3) E se nao houver pista na imagem? Ou no range tratado.
# Distance from the center
def distance_center(img):
    # Found the start and the end of lane in axis X
    start = end = 0
    already_found = False
    for i in range(Constants.WIDTH_IMAGE):
        if img[Constants.STRAIGHT_CENTER_ANALYSIS][i] == Constants.WHITE:
            end = i
            if not already_found:
                start = i
                already_found = True

    # Calculate the distance from the center. Measure: meters / pixel
    dist = end - start
    if dist != 0:
        scale = Constants.WIDTH_LANE / dist
    else:
        scale = 0
    center = (start + end) / 2
    distance_centimeters = (Constants.WIDTH_IMAGE/2 - center)*scale

    return distance_centimeters


# Alterar
def lane_detector(img_orig, img_processed):
    img_orig[img_processed == Constants.WHITE] = Constants.BLUE

    for i in range(Constants.HEIGHT_IMAGE):
        lane = True
        for j in range(Constants.WIDTH_IMAGE):
            if j-1 >= 0:
                if ((img_orig[i][j-1] == Constants.GREEN).all()) and (img_processed[i][j] == Constants.BLACK):
                    img_orig[i][j] = Constants.GREEN
                elif (img_processed[i][j-1] == Constants.WHITE) and (img_processed[i][j] == Constants.BLACK):
                    if lane:
                        img_orig[i][j] = Constants.GREEN
                        lane = False


# Determine the distance from the center and the curvature
def center_curvature(img):
    return 0, 0