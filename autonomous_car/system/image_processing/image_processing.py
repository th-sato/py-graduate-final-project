import cv2 as cv
import base64
import os.path
import numpy as np
from constants.constants import *

# Global variables
LOCAL_PATH = os.path.dirname(__file__)  # get current directory


def video_writer():
    fourcc = cv.VideoWriter_fourcc(*'MP4V')
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
        curv_text = 'Curvature cannot be calculated.'
    else:
        curvature = 1.0 / radius_curvature
        curv_text = 'Curvature = %.2f(m)' % curvature
    cv.putText(img, curv_text, (50, 50), font, 0.7, (255, 255, 255), 1)

    left_or_right = "left" if center > 0 else "right"
    cv.putText(img, 'Vehicle is %.2fcm %s of center' % (np.abs(center), left_or_right), (50, 100), font, 0.7,
                (255, 255, 255), 1)


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
def __disconsider_proximity_points(histogram, peak, space_lines):
    histogram_length = histogram.shape[0]  # Length of histogram

    # Left proximity
    if (peak - space_lines) < 0:
        histogram[0: peak] = 0
    else:
        histogram[(peak - space_lines): peak] = 0
    # Right proximity
    if (peak + space_lines) > (histogram_length - 1):
        histogram[peak: (histogram_length - 1)] = 0
    else:
        histogram[peak: (peak + space_lines)] = 0

    return histogram


def __take_histogram(img, interval):
    height_img = img.shape[0]
    boundary_histogram = np.int(height_img * interval[0]), np.int(height_img * interval[1])
    histogram = np.sum(img[boundary_histogram[0]: (boundary_histogram[1] - 1), :], axis=0)
    return histogram


def __find_peak_histogram(histogram, min_value):
    space_lines = 85  # Set the space between track lines
    peak = np.argmax(histogram) # Find one of the Peaks in Histogram
    peak_value = histogram[peak]  # Value of the peak one

    if peak_value > min_value:
        histogram = __disconsider_proximity_points(histogram, peak, space_lines)
        return histogram, peak
    else:
        return histogram, None


def __left_right_lane(peak_one, peak_two, search_in_end_of_img):
    if peak_one > peak_two:
        return peak_two, peak_one, search_in_end_of_img
    else:
        return peak_one, peak_two, search_in_end_of_img


def __find_peak_two(bin_warped, peak_one, hist, hist_min_value, interval_two):
    search_in_end_of_img = True
    peak_one_previous = peak_one
    # Search for other side
    _, peak_two = __find_peak_histogram(hist, hist_min_value)
    # Two size were found
    if peak_two is not None:
        return __left_right_lane(peak_one, peak_two, search_in_end_of_img)
    else:
        hist = __take_histogram(bin_warped, interval_two)
        hist, peak_one = __find_peak_histogram(hist, hist_min_value)
        if peak_one is not None:
            _, peak_two = __find_peak_histogram(hist, hist_min_value)
            if peak_two is not None:
                return __left_right_lane(peak_one, peak_two, (not search_in_end_of_img))
            else:
                # Discover if the peak is the left or the right
                if peak_one_previous > peak_one:
                    return None, peak_one_previous, search_in_end_of_img
                else:
                    return peak_one_previous, None, search_in_end_of_img
        else:
            interval = 0.7, 0.8571
            hist = __take_histogram(bin_warped, interval)
            _, peak_one = __find_peak_histogram(hist, hist_min_value)
            if peak_one_previous > peak_one:
                return None, peak_one_previous, search_in_end_of_img
            else:
                return peak_one_previous, None, search_in_end_of_img


def __find_peaks_of_image(binary_warped):
    histogram_min_value = 5  # Value to consider that the point is valid
    interval_middle = 0.5, 0.64
    interval_base = 0.8571, 1.0
    # interval_base = 0.5, 1.0
    histogram = __take_histogram(binary_warped, interval_base)
    histogram, peak_one = __find_peak_histogram(histogram, histogram_min_value)

    # One size of track was found
    if peak_one is not None:
        return __find_peak_two(binary_warped, peak_one, histogram, histogram_min_value, interval_middle)
    else:
        # histogram = __take_histogram(binary_warped, interval_middle)
        # histogram, peak_one = __find_peak_histogram(histogram, histogram_min_value)
        # if peak_one is not None:
        #     interval = 0.64, 0.75
        #     return __find_peak_two(binary_warped, peak_one, histogram, histogram_min_value, interval)
        # else:
        return None, None, False


def __window_boundaries(lane_indexes, window_x_current, window_y, nonzero_x, nonzero_y, margin, minpix):
    if window_x_current is None:
        return [], None

    win_x = window_x_current - margin, window_x_current + margin
    good_indexes = ((nonzero_y >= window_y[0]) & (nonzero_y < window_y[1]) & (nonzero_x >= win_x[0]) & (
                    nonzero_x < win_x[1])).nonzero()[0]
    lane_indexes.append(good_indexes)
    if len(good_indexes) > minpix:
        window_x_current = np.int(np.mean(nonzero_x[good_indexes]))

    return lane_indexes, window_x_current


def __fit_lines(lane_index, nonzero_x, nonzero_y):
    if len(lane_index) == 0:
        return None
    # Concatenate the arrays of indices
    lane_index = np.concatenate(lane_index)
    # Extract left and right line pixel positions
    x_positions = nonzero_x[lane_index]
    y_positions = nonzero_y[lane_index]

    return np.polyfit(y_positions, x_positions, 2)


# Functions for drawing lines
def fit_lines(binary_img):
    nwindows = 25                   # Choose the number of sliding windows
    margin = 30                     # Set the width of the windows +/- margin
    minpix = 10                     # Set minimum number of pixels found to recenter window
    # Create empty lists to receive left and right lane pixel indices
    left_lane_index = []
    right_lane_index = []
    binary_warped = binary_img
    height_img, width_img = binary_warped.shape

    # Find the peak of the left and right of image
    left_x_base, right_x_base, search_in_end_of_img = __find_peaks_of_image(binary_warped)

    # Set height of windows
    window_height = np.int((height_img / 2) / nwindows)
    # Identify the x and y positions of all nonzero pixels in the image
    nonzero = binary_warped.nonzero()
    nonzero_y = np.array(nonzero[0])
    nonzero_x = np.array(nonzero[1])

    # Current positions to be updated for each window
    left_x_current = left_x_base
    right_x_current = right_x_base

    # Point to start the search
    if search_in_end_of_img:
        height_img_base = height_img
    else:
        height_img_base = height_img / 2

    # Step through the windows one by one
    for window in range(nwindows):
        # Identify window boundaries in x and y (and right and left)
        if search_in_end_of_img:
            win_y = height_img_base - (window + 1) * window_height, height_img_base - window * window_height
        else:
            win_y = height_img_base + window * window_height, height_img_base + (window + 1) * window_height
        left_lane_index, left_x_current = __window_boundaries(left_lane_index, left_x_current, win_y, nonzero_x,
                                                              nonzero_y, margin, minpix)
        right_lane_index, right_x_current = __window_boundaries(right_lane_index, right_x_current, win_y, nonzero_x,
                                                                nonzero_y, margin, minpix)

    left_fit = __fit_lines(left_lane_index, nonzero_x, nonzero_y)
    right_fit = __fit_lines(right_lane_index, nonzero_x, nonzero_y)

    # out_img = np.dstack((binary_warped, binary_warped, binary_warped)) * 255
    # left_lane_index = np.concatenate(left_lane_index)
    # right_lane_index = np.concatenate(right_lane_index)
    # out_img[nonzero_y[left_lane_index], nonzero_x[left_lane_index]] = RED
    # out_img[nonzero_y[right_lane_index], nonzero_x[right_lane_index]] = BLUE
    # show_image(out_img)

    return left_fit, right_fit, (height_img, width_img)


def __lane_pixels(fit, plot_y):
    return fit[0] * plot_y ** 2 + fit[1] * plot_y + fit[2]


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
