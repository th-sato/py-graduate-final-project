import cv2 as cv
import os.path
import numpy as np
import system.constants.constants as CONSTANTS

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
def detect_yellow_street(img_hsv):
    yellow_range = np.array([20, 100, 100]), np.array([30, 255, 255])
    # define range of color (yellow) in HSV
    lower_color, upper_color = yellow_range
    # Threshold the HSV image to get only the selected colors
    img_lane = cv.inRange(img_hsv, lower_color, upper_color)
    return img_lane


# Functions for drawing lines
def fit_lines(binary_img):
    nwindows = 10  # Choose the number of sliding windows
    margin = 80  # Set the width of the windows +/- margin
    minpix = 70  # Set minimum number of pixels found to recenter window
    # Create empty lists to receive left and right lane pixel indices
    left_lane_inds = []
    right_lane_inds = []

    binary_warped = binary_img
    height_img, width_img = binary_warped.shape
    # Assuming you have created a warped binary image called "binary_warped"
    # Take a histogram of the bottom half of the image
    histogram = np.sum(binary_warped[height_img / 2:, :], axis=0)
    # Create an output image to draw on and  visualize the result
    out_img = np.dstack((binary_warped, binary_warped, binary_warped)) * 255
    # Find the peak of the left and right halves of the histogram
    # These will be the starting point for the left and right lines
    # Make this more robust
    midpoint = np.int(histogram.shape[0] / 2)
    left_x_base = np.argmax(histogram[0:midpoint])
    right_x_base = np.argmax(histogram[midpoint:(width_img - 1)]) + midpoint

    # Set height of windows
    window_height = np.int(height_img / nwindows)
    # Identify the x and y positions of all nonzero pixels in the image
    nonzero = binary_warped.nonzero()
    nonzero_y = np.array(nonzero[0])
    nonzero_x = np.array(nonzero[1])

    # Current positions to be updated for each window
    left_x_current = left_x_base
    right_x_current = right_x_base

    # Step through the windows one by one
    for window in range(nwindows):
        # Identify window boundaries in x and y (and right and left)
        win_y_low = binary_warped.shape[0] - (window + 1) * window_height
        win_y_high = binary_warped.shape[0] - window * window_height
        win_x_left_low = left_x_current - margin
        win_x_left_high = left_x_current + margin
        win_x_right_low = right_x_current - margin
        win_x_right_high = right_x_current + margin
        # Draw the windows on the visualization image
        # Identify the nonzero pixels in x and y within the window
        good_left_inds = ((nonzero_y >= win_y_low) & (nonzero_y < win_y_high) & (nonzero_x >= win_x_left_low) & (
                    nonzero_x < win_x_left_high)).nonzero()[0]
        good_right_inds = ((nonzero_y >= win_y_low) & (nonzero_y < win_y_high) & (nonzero_x >= win_x_right_low) & (
                    nonzero_x < win_x_right_high)).nonzero()[0]
        # Append these indices to the lists
        left_lane_inds.append(good_left_inds)
        right_lane_inds.append(good_right_inds)
        # If you found > minpix pixels, recenter next window on their mean position
        if len(good_left_inds) > minpix:
            left_x_current = np.int(np.mean(nonzero_x[good_left_inds]))
        if len(good_right_inds) > minpix:
            right_x_current = np.int(np.mean(nonzero_x[good_right_inds]))

    # Concatenate the arrays of indices
    left_lane_inds = np.concatenate(left_lane_inds)
    right_lane_inds = np.concatenate(right_lane_inds)

    # Extract left and right line pixel positions
    left_x = nonzero_x[left_lane_inds]
    left_y = nonzero_y[left_lane_inds]
    right_x = nonzero_x[right_lane_inds]
    right_y = nonzero_y[right_lane_inds]

    # Fit a second order polynomial to each
    left_fit = np.polyfit(left_y, left_x, 2)
    right_fit = np.polyfit(right_y, right_x, 2)

    out_img[nonzero_y[left_lane_inds], nonzero_x[left_lane_inds]] = [255, 0, 0]
    out_img[nonzero_y[right_lane_inds], nonzero_x[right_lane_inds]] = [0, 0, 255]

    return left_fit, right_fit, out_img


# Calculate Curvature
def curvature(left_fit, right_fit, binary_warped):
    xm_per_pix = CONSTANTS.axis_x_meters_per_pixel  # meters per pixel in x dimension
    ym_per_pix = CONSTANTS.axis_y_meters_per_pixel  # meters per pixel in y dimension
    height_img = binary_warped.shape[0]
    center_image = height_img / 2

    plot_y = np.linspace(0, height_img - 1, height_img)
    # Define y-value where we want radius of curvature
    # I'll choose the maximum y-value, corresponding to the bottom of the image
    y_eval = np.max(plot_y)

    # Define left and right lanes in pixels
    left_x = left_fit[0] * plot_y ** 2 + left_fit[1] * plot_y + left_fit[2]
    right_x = right_fit[0] * plot_y ** 2 + right_fit[1] * plot_y + right_fit[2]

    # Identify new coefficients in metres
    left_fit_cr = np.polyfit(plot_y * ym_per_pix, left_x * xm_per_pix, 2)
    right_fit_cr = np.polyfit(plot_y * ym_per_pix, right_x * xm_per_pix, 2)

    # Calculate the new radii of curvature
    left_curverad = ((1 + (2 * left_fit_cr[0] * y_eval * ym_per_pix + left_fit_cr[1]) ** 2) ** 1.5) / np.absolute(
        2 * left_fit_cr[0])
    right_curverad = ((1 + (2 * right_fit_cr[0] * y_eval * ym_per_pix + right_fit_cr[1]) ** 2) ** 1.5) / np.absolute(
        2 * right_fit_cr[0])

    # Calculation of center
    # left_lane and right lane bottom in pixels
    left_lane_bottom = (left_fit[0] * y_eval) ** 2 + left_fit[0] * y_eval + left_fit[2]
    right_lane_bottom = (right_fit[0] * y_eval) ** 2 + right_fit[0] * y_eval + right_fit[2]
    # Lane center as mid of left and right lane bottom

    lane_center = (left_lane_bottom + right_lane_bottom) / 2.
    center = (lane_center - center_image) * xm_per_pix  # Convert to meters

    return left_curverad, right_curverad, center
