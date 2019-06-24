# -*- coding: utf-8 -*-
"""
Created on Tue Oct 03 17:40:15 2017

@author: Camila
"""
"""
Spyder Editor

Controle do carro usado Logica Fuzzy para controlar o ângulo de guinada e a velocidade
"""

import os
os.chdir(r'/home/thiago/Dropbox/Faculdade/TCC/CamilaPereda')
import vrep
import math
import time
import cv2
from PIL import Image
import array
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from copy import deepcopy

#from moviepy.editor import VideoFileClip
from IPython.display import HTML

import pickle
import matplotlib.image as mpimg

# Funcoes

def grayscale(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Or use RGB2GRAY if you read an image with mpimg

def gaussian_blur(img, kernel_size):
    """Applies a Gaussian Noise kernel"""
    return cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)

def undistort(img):
    cal_pickle = pickle.load( open( "camera_cal/calibration_pickle2.p", "rb" ) )
    mtx = cal_pickle["mtx"]
    dist = cal_pickle["dist"]
    undist = cv2.undistort(img, mtx, dist, None, mtx)
    return undist

def x_thresh(img, sobel_kernel=3, thresh=(0, 255)):
    gray = grayscale(img)
    # Take only Sobel x 
    sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=sobel_kernel)
    #Calculate the absolute value of the x derivative:
    abs_sobelx = np.absolute(sobelx)
    #Convert the absolute value image to 8-bit:
    scaled_sobel = np.uint8(255*abs_sobelx/np.max(abs_sobelx))
    #Create binary image using thresholding
    sxbinary = np.zeros_like(scaled_sobel)
    sxbinary[(scaled_sobel >= thresh[0]) & (scaled_sobel <= thresh[1])] = 1
    return sxbinary

def mag_thresh(img, sobel_kernel=3, thresh=(0, 255)):
    # Convert to grayscale
    gray = grayscale(img)
    # Take both Sobel x and y gradients
    sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=sobel_kernel)
    sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=sobel_kernel)
    # Calculate the gradient magnitude
    gradmag = np.sqrt(sobelx**2 + sobely**2)
    # Rescale to 8 bit
    scale_factor = np.max(gradmag)/255 
    gradmag = (gradmag/scale_factor).astype(np.uint8) 
    # Create a binary image of ones where threshold is met, zeros otherwise
    binary_output = np.zeros_like(gradmag)
    binary_output[(gradmag >= thresh[0]) & (gradmag <= thresh[1])] = 1

    # Return the binary image
    return binary_output

def dir_threshold(img, sobel_kernel=3, thresh=(0, np.pi/2)):
    
    gray = grayscale(img)
    # Take both Sobel x and y gradients
    sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=sobel_kernel)
    sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=sobel_kernel)
    # Calculate the gradient magnitude
    abs_sobelx = np.absolute(sobelx)
    abs_sobely = np.absolute(sobely)
    
    dir_grad = np.arctan2(abs_sobely, abs_sobelx)
    
    binary_output = np.zeros_like(dir_grad)
    binary_output[(dir_grad >= thresh[0]) & (dir_grad <= thresh[1])] = 1
   
    return binary_output

def hsv_select(img, thresh_low, thresh_high):
    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    
    color_binary = np.zeros((img.shape[0], img.shape[1]))
    color_binary[(hsv[:,:,0] >= thresh_low[0]) & (hsv[:,:,0] <= thresh_high[0]) 
                  & (hsv[:,:,1] >= thresh_low[1])  & (hsv[:,:,1] <= thresh_high[1])  
                  & (hsv[:,:,2] >= thresh_low[2]) & (hsv[:,:,2] <= thresh_high[2])] = 1
    return color_binary 

def hls_select(img, thresh=(0, 255)):
    hls = cv2.cvtColor(img, cv2.COLOR_RGB2HLS)
    
    s = hls[:,:,2]
    s_binary = np.zeros_like(s)
    s_binary[(s > thresh[0]) & (s <= thresh[1])] = 1
    return s_binary

def warp(img):
    img_size = (img.shape[1], img.shape[0])
    
#    src = np.float32([[800,510],[1150,700],[270,700],[510,510]])
#    dst = np.float32([[650,470],[640,700],[270,700],[270,510]])
#    
    src = np.float32([[192,64],[250,250],[6,250],[64,64]])
    dst = np.float32([[192,64],[250,250],[6,250],[64,64]])
    
    M = cv2.getPerspectiveTransform(src, dst)
    
    #inverse 
    Minv = cv2.getPerspectiveTransform(dst, src)
    
    #create a warped image
    warped = cv2.warpPerspective(img, M, img_size, flags=cv2.INTER_LINEAR)
    
    unpersp = cv2.warpPerspective(warped, Minv, img_size, flags=cv2.INTER_LINEAR)
    
    return warped, unpersp, Minv


# Define a function for creating lane lines
def lane_detector(image, video_mode = False):
    #read image
#    if video_mode == False:
#        image = cv2.imread(image)
    
    # Undistort image
#    undist = undistort(image)
    undist = image
    #print(undist.shape)
    
    # Define a kernel size and apply Gaussian smoothing
    apply_blur = True
    if apply_blur:
        kernel_size = 5
        undist = gaussian_blur(undist, kernel_size)
    
    # Define parameters for gradient thresholding
    sxbinary = x_thresh(undist, sobel_kernel=3, thresh = (22,100)) #(22,100)
    mag_binary = mag_thresh(undist, sobel_kernel=3, thresh=(40, 100))
    dir_binary = dir_threshold(undist, sobel_kernel=15, thresh=(0.7, 1.3))
    
    # Define parameters for color thresholding
    s_binary = hls_select(undist, thresh=(90, 255))
    #You can combine various thresholding operations
    
    # Stack each channel to view their individual contributions in green and blue respectively
    # This returns a stack of the two binary images, whose components you can see as different colors
    color_binary = np.dstack(( np.zeros_like(sxbinary), sxbinary, s_binary))

    # Combine the two binary thresholds
    combined_binary1 = np.zeros_like(sxbinary)
    combined_binary1[(s_binary == 1) | (sxbinary == 1)] = 1
    
    combined_binary2 = np.zeros_like(sxbinary)
    combined_binary2[(s_binary == 1) | (sxbinary == 1)| (mag_binary == 1)] = 1
    
    # Apply perspective transform
    # Define points
    warped_im, _ , Minv = warp(combined_binary1)
    
    return undist, sxbinary, s_binary, combined_binary1, warped_im, Minv

#################################

# Functions for drawing lines 
def fit_lines(img, second_time, plot = True):

    # Set the width of the windows +/- margin
    margin = 45 #80
    # Set minimum number of pixels found to recenter window
    minpix = 250 #70
    
#    img = s_binary
    binary_warped = img
    # Assuming you have created a warped binary image called "binary_warped"
    # Take a histogram of the bottom half of the image
    histogram = np.sum(binary_warped[150:,:], axis=0)
#    histogram2 = np.append(np.sum(binary_warped[:,0:10], axis=0),np.zeros(246,dtype=int))
#    histogram3 = np.append(np.zeros(246,dtype=int),np.sum(binary_warped[:,246:], axis=0))
#    histogram = histogram1 + histogram2 + histogram3
#    histogram = np.sum(binary_warped, axis=0)
#    x = binary_warped[100:200,:]
#    plt.imshow(binary_warped[150:,:])
    # Create an output image to draw on and  visualize the result
    out_img = np.dstack((binary_warped, binary_warped, binary_warped))*255
#    plt.imshow(img, cmap = 'Greys_r')
    # Find the peak of the left and right halves of the histogram
    # These will be the starting point for the left and right lines
    #Make this more robust
    right = 0
    leftx_base = histogram.argmax()
    leftx_base_value = histogram[leftx_base]
    if leftx_base_value == 0:
        leftx_base = 45
        rightx_base = 210
        one_curve = False
    else:
        if leftx_base < 45:
            histogram[0:leftx_base+90] = 0
        else:
            histogram[leftx_base-45:leftx_base+45] = 0
        rightx_base = histogram.argmax()
        rightx_base_value = histogram[rightx_base]
        if rightx_base_value < 3:
            one_curve = True
        else:
            one_curve = False
        if leftx_base > rightx_base and one_curve == False:
            x = rightx_base
            rightx_base = leftx_base
            leftx_base = x
        if one_curve == True:
            histogram_left = sum(np.append(np.sum(binary_warped[:,0:10], axis=0),np.zeros(246,dtype=int)))
            histogram_right = sum(np.append(np.zeros(246,dtype=int),np.sum(binary_warped[:,246:], axis=0)))
            if histogram_left > histogram_right and leftx_base != 0:
                rightx_base = leftx_base
                leftx_base = 0
                right = 1
            else:
                rightx_base = 255
        if second_time == 1:
            one_curve = False
    # Choose the number of sliding windows
    nwindows = 10 #6
    # Set height of windows
    window_height = np.int((binary_warped.shape[0])/nwindows)
    # Identify the x and y positions of all nonzero pixels in the image
    nonzero = binary_warped.nonzero()
    nonzeroy = np.array(nonzero[0])
#    nonzeroy.sort()
#    nonzeroy = np.unique(nonzeroy)
    nonzerox = np.array(nonzero[1])
#    nonzerox.sort()
#    nonzerox = np.unique(nonzerox)
    if right == 0 or second_time == 1:
        # Current positions to be updated for each window
        leftx_current = leftx_base
        # Create empty lists to receive left and right lane pixel indices
        left_lane_inds = []
    if one_curve == False or right == 1:
        rightx_current = rightx_base
        right_lane_inds = []
    
    
#    window = 0
    
    # Step through the windows one by one
    for window in range(nwindows):
        # Identify window boundaries in x and y (and right and left)
        win_y_low = binary_warped.shape[0] - (window+1)*window_height
        win_y_high = binary_warped.shape[0] - window*window_height
        if right == 0 or second_time == 1:
            win_xleft_low = leftx_current - margin
            win_xleft_high = leftx_current + margin
        if one_curve == False or right == 1:
            win_xright_low = rightx_current - margin
            win_xright_high = rightx_current + margin
        if one_curve == False:
            if win_xleft_high>win_xright_low:
                middle = np.int((win_xleft_high+win_xright_low)/2)
                win_xleft_high = middle
                win_xright_low = middle
#               print middle
        if right == 0 or second_time == 1:
            # Draw the windows on the visualization image
            cv2.rectangle(out_img,(win_xleft_low,win_y_low),(win_xleft_high,win_y_high),(255,255,0), 2) 
        if one_curve == False or right == 1:
            cv2.rectangle(out_img,(win_xright_low,win_y_low),(win_xright_high,win_y_high),(0,255,0), 2) 
#        plt.imshow(out_img)
        if right == 0 or second_time == 1:
            # Identify the nonzero pixels in x and y within the window
            good_left_inds = ((nonzeroy >= win_y_low) & (nonzeroy < win_y_high) & (nonzerox >= win_xleft_low) & (nonzerox < win_xleft_high)).nonzero()[0]
        if one_curve == False or right == 1:
            good_right_inds = ((nonzeroy >= win_y_low) & (nonzeroy < win_y_high) & (nonzerox >= win_xright_low) & (nonzerox < win_xright_high)).nonzero()[0]
        if right == 0 or second_time == 1:
            # Append these indices to the lists
            left_lane_inds.append(good_left_inds)
        if one_curve == False or right == 1:
            right_lane_inds.append(good_right_inds)
        if right == 0 or second_time == 1:
            # If you found > minpix pixels, recenter next window on their mean position
            if len(good_left_inds) < minpix and len(good_left_inds) > 0:
                leftx_current = np.int(np.mean(nonzerox[good_left_inds])) 
        if one_curve == False or right == 1:
            if len(good_right_inds) < minpix and len(good_right_inds) > 0:        
                rightx_current = np.int(np.mean(nonzerox[good_right_inds]))
#        window = window + 1
    # Concatenate the arrays of indices
    if right == 0 or second_time == 1:
        left_lane_inds = np.concatenate(left_lane_inds)
    if one_curve == False or right == 1:
        right_lane_inds = np.concatenate(right_lane_inds)
    # Extract left and right line pixel positions
    if right == 0 or second_time == 1:
        leftx = nonzerox[left_lane_inds]
        lefty = nonzeroy[left_lane_inds] 
    if one_curve == False or right == 1:
        rightx = nonzerox[right_lane_inds]
        righty = nonzeroy[right_lane_inds] 

    ploty = np.linspace(0, binary_warped.shape[1]-1, binary_warped.shape[1] )
    
    if right == 0 or second_time == 1:
        # Fit a second order polynomial - left_line
        left_fit = np.polyfit(lefty, leftx, 2)
        
        # Generate x and y values for plotting - left_line
        left_fitx = left_fit[0]*ploty**2 + left_fit[1]*ploty + left_fit[2]
        out_img[nonzeroy[left_lane_inds], nonzerox[left_lane_inds]] = [255, 0, 0]
        left_fit_null = 1
    else:
        left_fit = 0
        left_fit_null = 0
    
    if one_curve == False or right == 1:
        # Fit a second order polynomial - right_line
        right_fit = np.polyfit(righty, rightx, 2)
        
        # Generate x and y values for plotting - right_line
        right_fitx = right_fit[0]*ploty**2 + right_fit[1]*ploty + right_fit[2]
        out_img[nonzeroy[right_lane_inds], nonzerox[right_lane_inds]] = [0, 0, 255]
        right_fit_null = 1
    else:
        right_fit = 0
        right_fit_null = 0
    
    if plot == True:
#        plt.figure(figsize=(10,10))
#        fig = plt.figure()

        plt.imshow(out_img)
        if right == 0 or second_time == 1:
            plt.plot(left_fitx, ploty, color='yellow')
        if one_curve == False:
            plt.plot(right_fitx, ploty, color='green')
        plt.xlim(0, 256)
        plt.ylim(155, 0)
    
    return left_fit, right_fit, left_fit_null, right_fit_null, out_img

#################################
#Calculate Curvature
def curvature(left_fit, right_fit, left_fit_null, right_fit_null, s_binary, print_data = True):
    ploty = np.linspace(0, s_binary.shape[1]-1, s_binary.shape[1] )
   
    # Define y-value where we want radius of curvature
    # I'll choose the maximum y-value, corresponding to the bottom of the image
#    y_eval = np.max(ploty)
    y_eval = 140 #240
    
#    ym_per_pix = 30.0/720 # meters per pixel in y dimension
#    xm_per_pix = 3.7/700 # meters per pixel in x dimension

    ym_per_pix = 7.0/256 # meters per pixel in y dimension
    xm_per_pix = 1.0/256 # meters per pixel in x dimension
    
    if left_fit_null != 0:
        #Define left and right lanes in pixels
        leftx = left_fit[0]*ploty**2 + left_fit[1]*ploty + left_fit[2]
        #Identify new coefficients in metres
        left_fit_cr = np.polyfit(ploty*ym_per_pix, leftx*xm_per_pix, 2)
        # Calculate the new radius of curvature    
        left_curverad = ((1 + (2*left_fit_cr[0]*y_eval*ym_per_pix + left_fit_cr[1])**2)**1.5) / (2*left_fit_cr[0])
        #left_lane and right lane bottom in pixels
        left_lane_bottom = left_fit[0]*y_eval**2 + left_fit[1]*y_eval + left_fit[2]
    else:
        left_curverad = 0
    if right_fit_null !=0:        
        #Define left and right lanes in pixels
        rightx = right_fit[0]*ploty**2 + right_fit[1]*ploty + right_fit[2]
        #Identify new coefficients in metres
        right_fit_cr = np.polyfit(ploty*ym_per_pix, rightx*xm_per_pix, 2)
        # Calculate the new radius of curvature    
        right_curverad = ((1 + (2*right_fit_cr[0]*y_eval*ym_per_pix + right_fit_cr[1])**2)**1.5) / (2*right_fit_cr[0])
        #left_lane and right lane bottom in pixels
        right_lane_bottom = right_fit[0]*y_eval**2 + right_fit[1]*y_eval + right_fit[2]
    else:
        right_curverad = 0
    
    
    # Calculate the new radii of curvature
    
    curve = (left_curverad + right_curverad)
    
    #Calculation of center

    # Lane center as mid of left and right lane bottom
    
    if right_fit_null == 0:
        lane_center = 256
    elif left_fit_null == 0:
        lane_center = 0
    else:
        curve = curve/2.0
        lane_center = (left_lane_bottom + right_lane_bottom)/2.
    center_image = 128
    center = (center_image - lane_center)*xm_per_pix #Convert to meters
    
    if print_data == True:
    #Now our radius of curvature is in meters
        print('Left curve ',left_curverad, 'm, Right curve ', right_curverad, 'm, Center', center, 'm, Curve ', curve, 'm')

    return left_curverad, right_curverad, center, curve, left_fit_null, right_fit_null

#################################
def add_text_to_image(img, cur, center):
    """
    Draws information about the center offset and the current lane curvature onto the given image.
    :param img:
    """

    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img, 'Radius of Curvature', (15, 25), font, 0.7, (255, 255, 255), 2)
    
    cv2.putText(img, '%d(m)' % cur, (80, 50), font, 0.7, (255, 255, 255), 2)

    left_or_right = "left" if center < 0 else "right"
    cv2.putText(img, 'Vehicle is %.2fm' % center, (25, 80), font, 0.7,
                (255, 255, 255), 2)
    
    cv2.putText(img, '%s of center' % (left_or_right), (25, 110), font, 0.7,
                (255, 255, 255), 2)

#################################
def draw_lines(undist, warped, left_fit, right_fit, curve, center, left_fit_null, right_fit_null, show_img = True ):
    # Create an image to draw the lines on
    warped = s_binary
    warp_zero = np.zeros_like(warped).astype(np.uint8)
    color_warp = np.dstack((warp_zero, warp_zero, warp_zero))
    
    ploty = np.linspace(0, warped.shape[1]-1, warped.shape[1] )
    if left_fit_null != 0:
        # Fit new polynomials to x,y in world space
        left_fitx = left_fit[0]*ploty**2+left_fit[1]*ploty+left_fit[2]
        # Recast the x and y points into usable format for cv2.fillPoly()
        pts_left = np.array([np.transpose(np.vstack([left_fitx, ploty]))])
        
    if right_fit_null != 0:
        right_fitx = right_fit[0]*ploty**2+right_fit[1]*ploty+right_fit[2] 
        pts_right = np.array([np.flipud(np.transpose(np.vstack([right_fitx, ploty])))])

    if left_fit_null != 0 and right_fit_null != 0:
        pts = np.hstack((pts_left, pts_right))
    else:
        if left_fit_null != 0:
            pts = pts_left
        else:
            pts = pts_right
        if curve > 0:
            pts = np.hstack((pts, ([[[256,205],[256,100]]])))    
        else:
            pts = np.hstack((pts, ([[[0,40],[0,150]]])))    
    # Draw the lane onto the warped blank image
    cv2.fillPoly(color_warp, np.int_([pts]), (0,0,255))

    # Warp the blank back to original image space using inverse perspective matrix (Minv)
    newwarp = cv2.warpPerspective(color_warp, Minv, (color_warp.shape[1], color_warp.shape[0])) 
    # Combine the result with the original image
    result = cv2.addWeighted(undist, 1, newwarp, 0.3, 0)
    add_text_to_image(result, curve, center)
    if show_img == True:
#        plt.figure(figsize=(10,10))
        fig = plt.figure()
        plt.imshow(result)
    
    return result



vrep.simxFinish(-1) # just in case, close all opened connections
clientID=vrep.simxStart('127.0.0.1',19999,True,True,5000,5) # Connect to V-REP

ErrorCode, steeringLeft = vrep.simxGetObjectHandle(clientID,'nakedCar_steeringLeft',vrep.simx_opmode_oneshot_wait)
ErrorCode, steeringRight = vrep.simxGetObjectHandle(clientID,'nakedCar_steeringRight',vrep.simx_opmode_oneshot_wait)
ErrorCode, motorLeft = vrep.simxGetObjectHandle(clientID,'nakedCar_motorLeft',vrep.simx_opmode_oneshot_wait)
ErrorCode, motorRight = vrep.simxGetObjectHandle(clientID,'nakedCar_motorRight',vrep.simx_opmode_oneshot_wait)
ErrorCode, vision_sensor = vrep.simxGetObjectHandle(clientID,'Vision_sensor',vrep.simx_opmode_oneshot_wait)
ErrorCode, leftdis = vrep.simxGetDistanceHandle(clientID,'left_dist',vrep.simx_opmode_oneshot_wait)
ErrorCode, rightdis = vrep.simxGetDistanceHandle(clientID,'right_dist',vrep.simx_opmode_oneshot_wait)
ErrorCode, totaldis = vrep.simxGetDistanceHandle(clientID,'total_dist',vrep.simx_opmode_oneshot_wait)
ErrorCode, car_size = vrep.simxGetDistanceHandle(clientID,'car_size',vrep.simx_opmode_oneshot_wait)
ErrorCode, disL = vrep.simxReadDistance(clientID,leftdis,vrep.simx_opmode_streaming)
ErrorCode, disR = vrep.simxReadDistance(clientID,rightdis,vrep.simx_opmode_streaming)
ErrorCode, dt = vrep.simxReadDistance(clientID,totaldis,vrep.simx_opmode_streaming)

desiredWheelRotSpeed = 10
r = 0.15
vel = desiredWheelRotSpeed*r*3.6
vrep.simxSetJointTargetVelocity(clientID,motorLeft,desiredWheelRotSpeed,vrep.simx_opmode_streaming)
vrep.simxSetJointTargetVelocity(clientID,motorRight,desiredWheelRotSpeed,vrep.simx_opmode_streaming)

d = 0.53
l = 0.68

#d=0.755
#l=2.5772

steeringAngleLeft = 0
steeringAngleRight = 0

vrep.simxSetJointTargetPosition(clientID,steeringLeft,steeringAngleLeft,vrep.simx_opmode_streaming)
vrep.simxSetJointTargetPosition(clientID,steeringRight,steeringAngleRight,vrep.simx_opmode_streaming)
time.sleep(2)


res,resolution,image = vrep.simxGetVisionSensorImage(clientID,vision_sensor,0,vrep.simx_opmode_streaming)
time.sleep(1)

desiredSteeringAngle = 0

###########################################
########### Fuzzy Control
###########################################

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# New Antecedent/Consequent objects hold universe variables and membership
########### Controle do angulo de guinada
# functions

distance = ctrl.Antecedent(np.arange(0, 0.5, 0.001), 'distance')
angle = ctrl.Consequent(np.arange(0, 0.45, 0.01), 'angle')

# Auto-membership function 

distance['center'] = fuzz.pimf(distance.universe, 0, 0.01, 0.02, 0.04)
distance['low_dist'] = fuzz.trimf(distance.universe, [0.02,0.05,0.1])
distance['medium_dist'] = fuzz.trimf(distance.universe, [0.05,0.10,0.2])
distance['high_dist'] = fuzz.pimf(distance.universe,0.15,0.2,0.4,0.5)
distance.view()

angle['zero'] = fuzz.pimf(angle.universe, 0, 0.02, 0.05, 0.07)
angle['low'] = fuzz.trimf(angle.universe, [0.03, 0.1, 0.25])
angle['medium'] = fuzz.trimf(angle.universe, [0.15, 0.25, 0.35])
angle['high'] = fuzz.trimf(angle.universe, [0.25, 0.35, 0.45])
angle.view()

# Regras

rule1 = ctrl.Rule(distance['center'], angle['zero'])
rule2 = ctrl.Rule(distance['low_dist'], angle['low'])
rule3 = ctrl.Rule(distance['medium_dist'], angle['medium'])
rule4 = ctrl.Rule(distance['high_dist'], angle['high'])

# Controle
angle_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4])

angle_LF = ctrl.ControlSystemSimulation(angle_ctrl)

########### Controle da velocidade
# functions

curv = ctrl.Antecedent(np.arange(0, 1000, 1), 'curv')
veloc = ctrl.Consequent(np.arange(-0.6, 0.6, 0.01), 'veloc')

# Auto-membership function

curv['high_curv'] = fuzz.trimf(curv.universe,[0,200,450])
curv['curv'] = fuzz.pimf(curv.universe,300,500,600,800)
curv['straight'] = fuzz.trimf(curv.universe, [600,800,1000])
curv.view()

veloc['low'] = fuzz.trimf(veloc.universe, [-0.6, -0.6, 0])
veloc['medium'] = fuzz.pimf(veloc.universe, -0.3, -0.15, 0.15, 0.3)
veloc['high'] = fuzz.trimf(veloc.universe, [0, 0.6, 0.6])
veloc.view()

# Regras

rule1 = ctrl.Rule(curv['high_curv'], veloc['low'])
rule2 = ctrl.Rule(curv['curv'], veloc['medium'])
rule3 = ctrl.Rule(curv['straight'], veloc['high'])

# Controle
veloc_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])

veloc_LF = ctrl.ControlSystemSimulation(veloc_ctrl)

j = 0
t = []
m_center = []
path_size = []
path_l = []
path_r = []
velocity = []
for i in range(100000):
    ErrorCode, disL = vrep.simxReadDistance(clientID,leftdis,vrep.simx_opmode_buffer)
    ErrorCode, disR = vrep.simxReadDistance(clientID,rightdis,vrep.simx_opmode_buffer)
#    ErrorCode, dt = vrep.simxReadDistance(clientID,totaldis,vrep.simx_opmode_buffer)
    ErrorCode, lt = vrep.simxReadDistance(clientID,car_size,vrep.simx_opmode_buffer)
    res,resolution,image = vrep.simxGetVisionSensorImage(clientID,vision_sensor,0,vrep.simx_opmode_buffer)
    img = np.array(image, dtype = np.uint8)
    img.resize([resolution[0], resolution[1], 3])
    img = np.rot90(img,2)
    img = np.fliplr(img)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    img = img[50:255,:]
    k = 1
    dt = lt + disL + disR
    path_size.append(dt)
    path_l.append(-dt/2)
    path_r.append(dt/2)
    measure_center = (disL+(dt-disR))/2 - dt/2
    t.append(i*0.1)
    m_center.append(measure_center)
    print ("Center: " + str(measure_center))
#    mpimg.imsave(str(j)+".jpg",img)
#    j += 1

    
#    os.chdir(r'C:\Users\Camila\Documents\ITA\3 ELE\TG\V-REP\etapa 2')
    
#    image = 'image processing/DB3/'+str(i)+'.jpg'
#    img = cv2.imread(image)
    
#    plt.imshow(img)    
#    print i

        
#    try:
#    cv2.imshow('Image', img)
#    tecla = cv2.waitKey(10) & 0xFF
#    if tecla == 27: 
#        break
    try:
        print (j)
#        undist, sxbinary, s_binary, combined_binary1, warped_im, Minv = lane_detector(img)
#        left_fit, right_fit, right_fit_null, out_img = fit_lines(s_binary, plot= False)
#        left_cur, right_cur, center, curve, right_fit_null = curvature(left_fit, right_fit, right_fit_null, s_binary, print_data = False)
#        result  = draw_lines(undist, s_binary, left_fit, right_fit, curve, center, right_fit_null, show_img = False)
#    
        undist, sxbinary, s_binary, combined_binary1, warped_im, Minv = lane_detector(img)
        left_fit, right_fit, left_fit_null, right_fit_null, out_img = fit_lines(s_binary, 0, plot= False)
        left_cur, right_cur, center, curve, left_fit_null, right_fit_null = curvature(left_fit, right_fit, left_fit_null, right_fit_null, s_binary, print_data = False)
        if abs(curve) > 500 and (right_fit_null == 0 or left_fit_null == 0):
            left_fit, right_fit, left_fit_null, right_fit_null, out_img = fit_lines(s_binary, 1, plot= False)
            left_cur, right_cur, center, curve, left_fit_null, right_fit_null = curvature(left_fit, right_fit, left_fit_null, right_fit_null, s_binary, print_data = False)
        result  = draw_lines(undist, s_binary, left_fit, right_fit, curve, center, left_fit_null, right_fit_null, show_img = False)
        
        cv2.imshow('Image', result)
        tecla = cv2.waitKey(10) & 0xFF
        if tecla == 27: 
            break
        
        input_distance = abs(center)
        
        angle_LF.input['distance'] = input_distance
        # Crunch the numbers
        angle_LF.compute()
        
        desiredSteeringAngle = angle_LF.output['angle']*abs(center)/center
        print ('Angle' + str(desiredSteeringAngle))
        print ('-----------')
        if desiredSteeringAngle == 0:
            steeringAngleLeft = 0
            steeringAngleRight = 0
        elif desiredSteeringAngle > 0:
            steeringAngleLeft=math.tan(l/(-d+l/math.tan(desiredSteeringAngle)))
            steeringAngleRight=math.atan(l/(d+l/math.tan(desiredSteeringAngle)))
        else:
            steeringAngleRight=-math.tan(l/(-d+l/math.tan(-desiredSteeringAngle)))
            steeringAngleLeft=-math.atan(l/(d+l/math.tan(-desiredSteeringAngle)))
    
    #        angle.view(sim=tipping)
    
    #        print j
    #        mpimg.imsave(str(j)+".jpg",img)
    #        mpimg.imsave(str(j)+"_output.jpg",result)
    #        j += 1   
    #        
        
        veloc_LF.input['curv'] = abs(curve)
        # Crunch the numbers
        veloc_LF.compute()
        
        
        desiredWheelRotSpeed = desiredWheelRotSpeed + veloc_LF.output['veloc']
        if desiredWheelRotSpeed > 18:
            desiredWheelRotSpeed = 18
        if desiredWheelRotSpeed < 12:
            desiredWheelRotSpeed = 12
        vel = desiredWheelRotSpeed*r*3.6
        
        vrep.simxSetJointTargetPosition(clientID,steeringLeft,steeringAngleLeft,vrep.simx_opmode_streaming)
        vrep.simxSetJointTargetPosition(clientID,steeringRight,steeringAngleRight,vrep.simx_opmode_streaming)
        vrep.simxSetJointTargetVelocity(clientID,motorLeft,desiredWheelRotSpeed,vrep.simx_opmode_streaming)
        vrep.simxSetJointTargetVelocity(clientID,motorRight,desiredWheelRotSpeed,vrep.simx_opmode_streaming)
        k = 1
        print ('vel: ' + str(vel))
        print (' -----')
    except:
        k = k + 1
        print ("Image processing FAILED")
        if k == 4:
            vrep.simxPauseSimulation(clientID,vrep.simx_opmode_oneshot)
    velocity.append(vel)
    time.sleep(0.1)
    
cv2.destroyAllWindows()

plt.plot(t,m_center)
plt.axis([5, t[-1], -0.5, 0.5])
#plt.plot(t,path_r)
#plt.plot(t,path_l)
plt.xlabel('Time (s)')
plt.ylabel('Distance (m)')
plt.show()

np.std(m_center)
np.mean(m_center)

plt.plot(t,velocity)
plt.axis([0, t[-1], 5, 11])
plt.xlabel('Time (s)')
plt.ylabel('Velocity (m/s)')
plt.show()
