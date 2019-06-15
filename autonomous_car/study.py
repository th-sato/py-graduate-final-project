#####################################################################################################################
#################################################### Controller #####################################################
#####################################################################################################################
# from system.controller.fuzzy_controller import *
# from system.image_processing.image_processing import *
# import matplotlib.pyplot as plt
#
#
# def main():
#     print "Iniciando..."
#     fuzzy = FuzzyController()
#     distance_center = 0.04
#     curvature = 0.0
#     fuzzy.distance.view()
#     # fuzzy.angle.view()
#     # fuzzy.radius_curvature.view()
#     # fuzzy.speed.view()
#
#     # for i in range(550):
#     #     speed, angle = fuzzy.output((i + 1) / 1000.0, 0)
#     #     print (i + 1) / 1000.0, speed, angle
#     # value = 450 / 1000.0
#
#     speed, angle = fuzzy.output(distance_center, curvature)
#     print "distance_center: ", distance_center, ", angle:", angle, ", curvature: ", curvature, ", speed: ", speed
#     fuzzy.angle.view(sim=fuzzy.angle_control_system)
#     # fuzzy.speed.view(sim=fuzzy.speed_control_system)
#     print "Finalizando..."
#
#
# if __name__ == "__main__":
#     main()
#     plt.show()
#


#####################################################################################################################
###################################################### Teste 2 ######################################################
#####################################################################################################################

# from system.image_processing.image_processing import *
# import os
# static_path = 'images-test/2019-03-25/'
# image_name = 'pista-camera1.jpg'

# def get_image():
#     img_path = os.path.join(os.getcwd(), static_path)
#     return cv.imread(os.path.join(img_path, image_name))

from system.controller.fuzzy_controller import FuzzyController
from system.image_processing.image_processing import *
import matplotlib.pyplot as plt

# static_path = '../images-test/2019-05-04/'
# image_name = [
#     'carro_fora_pista.jpg',
#     'carro_fora_pista_2.jpg',
#     'duas_pistas.jpg',
#     'duas_pistas_2.jpg',
#     'pista_parcial.jpg',
#     'uma_pista.jpg',
#     'uma_pista_2.jpg'
# ]

# static_path = '../images-test/2019-05-26/'
# image_name = [
#     'teste1.png',
#     # 'teste2.png',
# ]

# static_path = '../images-test/2019-06-08/'
# image_name = [
#     'teste1.jpg',
#     'teste2.jpg',
# ]

static_path = '../images-test/2019-06-14/'
image_name = [
    # 'erro1.jpg',
    # 'erro2.jpg',
    # 'erro3.jpg',
    'erro4.jpg',
]


def detect_street_by_color(video):
    lower_color, upper_color = np.array([20, 0, 100]), np.array([30, 255, 255])
    return detect_street(video, lower_color, upper_color)


def image_input(name):
    img_path = os.path.join(os.path.join(os.getcwd(), static_path), name)
    img = cv.imread(img_path)
    return img


def plot_image(fit, ploty):
    plt.figure()
    plt.plot(fit, ploty, color='black')


def main():
    for name in image_name:
        print "name:", name
        img = image_input(name)
        img_processed = detect_street_by_color(img)
        img_test = img_processed.copy()
        nonzero = img_test.nonzero()
        img_test[img_processed == 1] = 255
        show_image(img_test)
        left_fit, right_fit, video_shape = fit_lines(img_processed)
        left_cur, right_cur, left_x, right_x, distance_center = curvature(left_fit, right_fit, video_shape)
        video_road = draw_lines(img, left_x, right_x)
        # if left_x is not None:
        #     plot_image(left_x, plot_y)
        # if right_x is not None:
        #     plot_image(right_x, plot_y)
        # curv = (left_cur + right_cur) / 2
        # add_text_to_image(video_road, curv, distance_center)
        curv = (left_cur + right_cur) / 2
        add_text_to_image(video_road, curv, distance_center)
        show_image(video_road)


if __name__ == "__main__":
    main()


#####################################################################################################################
###################################################### Teste 1 ######################################################
#####################################################################################################################

# def main2():
#     fuzzy = FuzzyController()
#     # fuzzy.distance.view()
#     # raw_input("Press Enter to continue...")
#     # fuzzy.angle.view()
#     # raw_input("Press Enter to continue...")
#     print "Output: ", fuzzy.output(1.555555555555, 0.0)
#
#     # img = get_image()
#     # show_image(img)
#
#     # img_processed = detect_street(img)
#     # _, _, img_processed = fit_lines(img_processed)
#     # show_image(img_processed)


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


