from system.image_processing.image_processing import *
from constants.constants import FUZZY_CONTROLLER, PROPORCIONAL_CONTROLLER
from autonomous_car import AutonomousCar
import os

static_path = '../images-test/2019-03-25/'
image_name = 'pista-camera1.jpg'
autonomous_car = AutonomousCar(FUZZY_CONTROLLER)


def get_image():
    img_path = os.path.join(os.getcwd(), static_path)
    return cv.imread(os.path.join(img_path, image_name))


def main():
    img = get_image()
    img_processed = detect_street(img)
    _, _, img_processed = fit_lines(img_processed)
    show_image(img_processed)


if __name__ == "__main__":
    main()



# import system.system as system
# import cv2 as cv
# import numpy as np
# import os

# static_path = 'images-test/2019-03-25/'
# image_name = 'pista-camera1.jpg'
#
#
# def detect_yellow_street(img_hsv):
#     # define range of color (yellow) in HSV
#     lower_color, upper_color = np.array([20, 0, 100]), np.array([30, 255, 255])
#     # lower_color, upper_color = np.array([20, 100, 100]), np.array([30, 255, 255])
#     # Threshold the HSV image to get only the selected colors
#     # img_lane = cv.GaussianBlur(img_hsv, (5, 5), 0)
#     img_lane = cv.inRange(img_hsv, lower_color, upper_color)
#     # img_lane[img_lane[240:420,:]] = 0
#     # img_lane[img_lane == 255] = 1
#
#     # element = cv.getStructuringElement(cv.MORPH_RECT, (4, 4))
#     # img_lane = cv.erode(img_lane, element)
#
#     cv.imshow('image', img_lane)
#     cv.waitKey(0)
#     cv.destroyAllWindows()
#
#     return img_lane
#
#
# def detect_street(img):
#     interval = img.shape[0]//2, int(img.shape[0]*(1.0 - 1.0/8.0))
#     img_hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
#     # img_processed = detect_yellow_street(img_hsv)
#     img_processed = detect_yellow_street(img_hsv[interval[0]:interval[1], :])
#     return img_processed
#
#
# # Functions for drawing lines
# def fit_lines(binary_img):
#     nwindows = 50  # Choose the number of sliding windows
#     margin = 30  # Set the width of the windows +/- margin
#     minpix = 10  # Set minimum number of pixels found to recenter window
#     # Create empty lists to receive left and right lane pixel indices
#     left_lane_inds = []
#     right_lane_inds = []
#
#     binary_warped = binary_img
#     height_img, width_img = binary_warped.shape
#     # Assuming you have created a warped binary image called "binary_warped"
#     # Take a histogram of the bottom half of the image
#     test_image = binary_warped[height_img / 2:, :]
#     # test_image = binary_warped
#     print test_image.shape
#     show_image(test_image)
#     histogram = np.sum(test_image, axis=0)
#     # Create an output image to draw on and  visualize the result
#     out_img = np.dstack((binary_warped, binary_warped, binary_warped)) * 255
#     # Find the peak of the left and right halves of the histogram
#     # These will be the starting point for the left and right lines
#     # Make this more robust
#     midpoint = np.int(histogram.shape[0] / 2)
#     left_x_base = np.argmax(histogram[0:midpoint])
#     right_x_base = np.argmax(histogram[midpoint:(width_img - 1)]) + midpoint
#
#     # Set height of windows
#     window_height = np.int(height_img / nwindows)
#     # Identify the x and y positions of all nonzero pixels in the image
#     nonzero = binary_warped.nonzero()
#     nonzero_y = np.array(nonzero[0])
#     nonzero_x = np.array(nonzero[1])
#
#     # Current positions to be updated for each window
#     left_x_current = left_x_base
#     right_x_current = right_x_base
#
#     # Step through the windows one by one
#     for window in range(nwindows):
#         # Identify window boundaries in x and y (and right and left)
#         win_y_low = binary_warped.shape[0] - (window + 1) * window_height
#         win_y_high = binary_warped.shape[0] - window * window_height
#         win_x_left_low = left_x_current - margin
#         win_x_left_high = left_x_current + margin
#         win_x_right_low = right_x_current - margin
#         win_x_right_high = right_x_current + margin
#         # Draw the windows on the visualization image
#         # Identify the nonzero pixels in x and y within the window
#         good_left_inds = ((nonzero_y >= win_y_low) & (nonzero_y < win_y_high) & (nonzero_x >= win_x_left_low) & (
#                     nonzero_x < win_x_left_high)).nonzero()[0]
#         good_right_inds = ((nonzero_y >= win_y_low) & (nonzero_y < win_y_high) & (nonzero_x >= win_x_right_low) & (
#                     nonzero_x < win_x_right_high)).nonzero()[0]
#         # Append these indices to the lists
#         left_lane_inds.append(good_left_inds)
#         right_lane_inds.append(good_right_inds)
#         # If you found > minpix pixels, recenter next window on their mean position
#         if len(good_left_inds) > minpix:
#             left_x_current = np.int(np.mean(nonzero_x[good_left_inds]))
#         if len(good_right_inds) > minpix:
#             right_x_current = np.int(np.mean(nonzero_x[good_right_inds]))
#
#     # Concatenate the arrays of indices
#     left_lane_inds = np.concatenate(left_lane_inds)
#     right_lane_inds = np.concatenate(right_lane_inds)
#
#     # Extract left and right line pixel positions
#     left_x = nonzero_x[left_lane_inds]
#     left_y = nonzero_y[left_lane_inds]
#     right_x = nonzero_x[right_lane_inds]
#     right_y = nonzero_y[right_lane_inds]
#
#     # Fit a second order polynomial to each
#     left_fit = np.polyfit(left_y, left_x, 2)
#     right_fit = np.polyfit(right_y, right_x, 2)
#
#     out_img[nonzero_y[left_lane_inds], nonzero_x[left_lane_inds]] = [255, 0, 0]
#     out_img[nonzero_y[right_lane_inds], nonzero_x[right_lane_inds]] = [0, 0, 255]
#
#     return left_fit, right_fit, out_img
#
#
# def show_image(img):
#     cv.imshow('image', img)
#     cv.waitKey(0)
#     cv.destroyAllWindows()
#
#
# def main():
#     img_path = os.path.join(os.getcwd(), static_path)
#     img = cv.imread(os.path.join(img_path, image_name))
#     img_processed = detect_street(img)
#     # Shape of image is accessed by img.shape.
#     # It returns a tuple of number of rows, columns and channels (if image is color)
#     # height, width = img.shape
#     _, _, img_processed = fit_lines(img_processed)
#
#     # cv.imshow('image', img)
#     # cv.waitKey(0)
#     # cv.destroyAllWindows()
#
#     cv.imshow('image', img_processed)
#     cv.waitKey(0)
#     cv.destroyAllWindows()
#
#
# if __name__ == "__main__":
#     main()


