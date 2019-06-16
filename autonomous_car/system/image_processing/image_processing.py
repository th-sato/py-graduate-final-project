# -*- coding: utf-8 -*-
import cv2 as cv
import base64
import os.path
import numpy as np
from env.constants import *

# Global variables
LOCAL_PATH = os.path.dirname(__file__)  # get current directory


def video_writer():
    # fourcc = cv.VideoWriter_fourcc(*'X264')
    fourcc = 0X00000021
    return cv.VideoWriter(VIDEO_NAME, fourcc, 20.0, (WIDTH_IMAGE, HEIGHT_IMAGE))


def show_image(img):
    cv.imshow('image', img)
    # cv.waitKey(10)
    cv.waitKey(0)
    # cv.destroyAllWindows()


def jpgimg_to_base64(img):
    ret, jpg = cv.imencode('.jpg', img)
    return base64.b64encode(jpg)


def add_text_to_image(img, radius_curvature, center):
    font = cv.FONT_HERSHEY_SIMPLEX
    if radius_curvature == 0:
        curv_text = 'Curvatura nao pode ser calculada.'
    else:
        curvature = 1.0 / radius_curvature
        curv_text = 'Curvatura = %.2f(m)' % curvature
    cv.putText(img, curv_text, (50, 50), font, 0.7, (255, 255, 255), 1)

    left_or_right = "esquerda" if center > 0 else "direita"
    cv.putText(img, 'Veiculo esta %.2fm a %s do centro' % (np.abs(center), left_or_right), (50, 100), font, 0.7,
                (255, 255, 255), 1)


# Get the pixels of function
# fit: function
# plot_y: points to get the pixels
def __lane_pixels(fit, plot_y):
    return fit[0] * plot_y ** 2 + fit[1] * plot_y + fit[2]


# img_binary contains only 0 or 255
def detect_street(img, lower_color, upper_color):
    img_hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    # interval = img.shape[0] / 2, int(img.shape[0] * (1.0 - 1.0 / 8.0))
    # img_hsv = img_hsv[interval[0]:interval[1], :]
    # Threshold the HSV image to get only the selected colors
    img_processed = cv.inRange(img_hsv, lower_color, upper_color)
    img_processed[img_processed == 255] = 1
    return img_processed


# Disconsider the proximity points of peak_one
# space_lines: the space between track lines
def __disconsider_proximity_points(histogram, peak, space_lines=85):
    histogram_length = histogram.shape[0]  # Length of histogram

    # Left proximity
    if (peak - space_lines) < 0:
        histogram[0: peak] = 0
    else:
        histogram[(peak - space_lines): peak] = 0
    # Right proximity
    if (peak + space_lines) > (histogram_length - 1):
        histogram[peak: histogram_length] = 0
    else:
        histogram[peak: (peak + space_lines)] = 0

    return histogram


# Return the histogram
def __take_histogram(img, x=None, y=None):
    if (x is None) and (y is None):
        return None

    if x is None:
        return np.sum(img[y[0]: y[1], :], axis=0)
    elif y is None:
        return np.sum(img[:, x[0]: x[1]], axis=0)
    else:
        return np.sum(img[y[0]: y[1], x[0]: x[1]], axis=0)


# Search for peaks of histogram
# min_value: value to consider a peak
def __search_for_peak_histogram(histogram, min_value=5):
    peak = np.argmax(histogram)   # Find one of the Peaks in Histogram
    peak_value = histogram[peak]  # Value of the peak one

    if peak_value >= min_value:
        histogram = __disconsider_proximity_points(histogram, peak)
        return histogram, peak
    else:
        return histogram, None


# Sliding window algorithm
# nwindows: Choose the number of sliding windows
# margin: Set the width of the windows +/- margin
# minpix: Set minimum number of pixels found to recenter window
# lane_index: Create empty lists to receive lane pixel indices
def __sliding_window_algorithm(nonzero, interval_y, x_base, nwindows=30, margin=30, minpix=10,
                               x_pos=[], y_pos=[], bin_img=None):
    lane_index = []
    # Check if the point is being passed
    if x_base is None:
        return None
    x_current = x_base
    nonzero_y = np.array(nonzero[0])
    nonzero_x = np.array(nonzero[1])

    window_height = np.int((interval_y[1] - interval_y[0]) / nwindows)

    for window in range(nwindows):
        # Identify window boundaries in x and y (and right and left)
        win_y = interval_y[1] - (window + 1) * window_height, interval_y[1] - window * window_height
        # Window boundaries
        win_x = x_current - margin, x_current + margin
        good_indexes = ((nonzero_y >= win_y[0]) & (nonzero_y < win_y[1]) & (nonzero_x >= win_x[0]) &
                        (nonzero_x < win_x[1])).nonzero()[0]
        lane_index.append(good_indexes)
        if len(good_indexes) > minpix:
            x_current = np.int(np.mean(nonzero_x[good_indexes]))

    # Least squares polynomial fit
    # Concatenate the arrays of indices
    lane_index = np.concatenate(lane_index)
    if len(lane_index) == 0 and x_pos == [] and y_pos == []:
        return None
    # Extract left and right line pixel positions
    x_positions = np.append(x_pos, nonzero_x[lane_index])
    y_positions = np.append(y_pos, nonzero_y[lane_index])

    if bin_img is not None:
        out_img = np.dstack((bin_img, bin_img, bin_img)) * 255
        out_img[nonzero_y[lane_index], nonzero_x[lane_index]] = RED
        show_image(out_img)

    return np.polyfit(y_positions, x_positions, 2)

# def __sliding_window_algorithm(nonzero, interval_y, x_base, nwindows=20, margin=30, minpix=10):
#     out_img = np.dstack((binary_img, binary_img, binary_img)) * 255
#     out_img[nonzero_y[lane_index], nonzero_x[lane_index]] = RED
#     show_image(out_img)


# Functions for found the functions of lines
def fit_lines(binary_img, straight_value=0.0004):
    # Histogram -- Half of image
    height_img, width_img = binary_img.shape
    half_height = np.int(0.4 * height_img)
    first_interval_y = [half_height, height_img]
    histogram = __take_histogram(binary_img, y=[np.int(0.9 * height_img), height_img])

    # Search for two peaks
    histogram, peak_one = __search_for_peak_histogram(histogram)
    histogram, peak_two = __search_for_peak_histogram(histogram)

    # Identify the x and y positions of all nonzero pixels in the image
    nonzero = binary_img.nonzero()

    if (peak_one is not None) and (peak_two is not None):
        left_x_base, right_x_base = (peak_one, peak_two) if peak_two > peak_one else (peak_two, peak_one)
        left_fit = __sliding_window_algorithm(nonzero, first_interval_y, left_x_base)
        right_fit = __sliding_window_algorithm(nonzero, first_interval_y, right_x_base)
    # Determine the right and left base of lines
    elif peak_one is not None:
        x_fit = __sliding_window_algorithm(nonzero, first_interval_y, peak_one)
        x_fit_base_img = __lane_pixels(x_fit, height_img - 1)
        # Histogram from extremity of image
        interval_y = [half_height, np.int(0.8 * height_img)]
        interval_x = [0, np.int(0.1 * width_img)], [np.int(0.9 * width_img), width_img - 1]
        left_hist = __take_histogram(binary_img, y=interval_y, x=interval_x[0])
        right_hist = __take_histogram(binary_img, y=interval_y, x=interval_x[1])
        # Get peak in histogram
        _, peak_x_left = __search_for_peak_histogram(left_hist, min_value=4)
        _, peak_x_right = __search_for_peak_histogram(right_hist, min_value=4)
        if peak_x_right is not None:
            peak_x_right = peak_x_right + interval_x[1][0]

        # Check if the lane is straight
        is_straight = True if np.absolute(x_fit[0]) < straight_value else False

        if x_fit[0] > 0:  # Right direction
            if peak_x_left is not None:
                left_x_base = peak_x_left
                right_fit = x_fit
                other_lane_base_x = x_fit_base_img - WIDTH_LANE_PIXEL
                left_fit = __sliding_window_algorithm(nonzero, interval_y, left_x_base, minpix=4,
                                                      x_pos=other_lane_base_x, y_pos=height_img-1)
            elif is_straight and peak_x_right is not None:
                left_fit = x_fit
                right_x_base = peak_x_right
                other_lane_base_x = x_fit_base_img + WIDTH_LANE_PIXEL
                right_fit = __sliding_window_algorithm(nonzero, interval_y, right_x_base, minpix=4,
                                                       x_pos=other_lane_base_x, y_pos=height_img-1)
            else:
                left_fit = x_fit
                right_fit = None
        else:  # Left direction
            if peak_x_right is not None:
                right_x_base = peak_x_right
                left_fit = x_fit
                other_lane_base_x = x_fit_base_img + WIDTH_LANE_PIXEL
                right_fit = __sliding_window_algorithm(nonzero, interval_y, right_x_base,
                                                       x_pos=other_lane_base_x, y_pos=height_img-1)
            elif is_straight and peak_x_left is not None:
                right_fit = x_fit
                left_x_base = peak_x_left
                other_lane_base_x = x_fit_base_img - WIDTH_LANE_PIXEL
                left_fit = __sliding_window_algorithm(nonzero, interval_y, left_x_base,
                                                      x_pos=other_lane_base_x, y_pos=height_img-1)
            else:
                left_fit = None
                right_fit = x_fit

    else:
        left_fit, right_fit = None, None

    return left_fit, right_fit, (height_img, width_img)


def __curvature_lane(fit, plot_y, ym_per_pix, xm_per_pix):
    if fit is None:
        return None, 0, None

    # Define y-value where we want radius of curvature
    # I'll choose the maximum y-value, corresponding to the bottom of the image
    y_eval = np.max(plot_y)
    # Define lanes in pixels
    lane_pixels = __lane_pixels(fit, plot_y)
    # Lane bottom in pixels
    point_bottom = __lane_pixels(fit, y_eval)
    # Identify new coefficients in meters
    fit_cr = np.polyfit(plot_y * ym_per_pix, lane_pixels * xm_per_pix, 2)
    # Calculate the new radius of curvature
    radius = ((1 + (2 * fit_cr[0] * y_eval * ym_per_pix + fit_cr[1]) ** 2) ** 1.5) / np.absolute(2 * fit_cr[0])

    return point_bottom, radius, lane_pixels


# Calculate Curvature
def curvature(left_fit, right_fit, image_shape):
    xm_per_pix = AXIS_X_METERS_PER_PIXEL  # meters per pixel in x dimension
    ym_per_pix = AXIS_Y_METERS_PER_PIXEL  # meters per pixel in y dimension
    height_img, width_img = image_shape
    pixels_lane = WIDTH_LANE_PIXEL
    center_image = width_img / 2

    plot_y = np.linspace(0, height_img - 1, height_img)

    left_point_bottom, left_radius, left_x = __curvature_lane(left_fit, plot_y, ym_per_pix, xm_per_pix)
    right_point_bottom, right_radius, right_x = __curvature_lane(right_fit, plot_y, ym_per_pix, xm_per_pix)

    # Lane center as mid of left and right lane bottom
    if left_point_bottom is None:
        left_point_bottom = right_point_bottom - pixels_lane
    if right_point_bottom is None:
        right_point_bottom = left_point_bottom + pixels_lane

    lane_center = (left_point_bottom + right_point_bottom) / 2.0
    distance_center = (lane_center - center_image) * xm_per_pix  # Convert to meters

    return left_radius, right_radius, left_x, right_x, distance_center


def draw_lines(img, left_fit_x, right_fit_x):
    height_img, width_img, _ = img.shape
    # Create an image to draw the lines on
    img_zeros = np.zeros_like(img)

    plot_y = np.linspace(0, img.shape[0] - 1, img.shape[0])

    # Recast the x and y points into usable format for cv2.fillPoly()
    if left_fit_x is not None:
        pts_left = np.array([np.transpose(np.vstack([left_fit_x, plot_y]))])

    if right_fit_x is not None:
        pts_right = np.array([np.flipud(np.transpose(np.vstack([right_fit_x, plot_y])))])

    if (left_fit_x is not None) and (right_fit_x is not None):
        pts = np.hstack((pts_left, pts_right))
    elif left_fit_x is None:
        pts = np.hstack((([[[0, 0], [0, height_img-1]]]), pts_right))
    elif right_fit_x is None:
        pts = np.hstack((pts_left, ([[[width_img-1, height_img-1], [width_img-1, 0]]])))

    # Draw the lane onto the warped blank image
    cv.fillPoly(img_zeros, np.array([pts], dtype=np.int32), GREEN)
    return cv.addWeighted(img, 1, img_zeros, 0.8, 0)
