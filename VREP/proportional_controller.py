# -*- coding: utf-8 -*-
"""
Created on Tue Oct 03 17:40:15 2017

@author: Camila
"""

import os
os.chdir(r'/home/thiago/Documentos/TCC/Sato')
import vrep
import math
import time
import cv2
from PIL import Image
import array
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from image_processing import *

#from moviepy.editor import VideoFileClip
from IPython.display import HTML

import pickle
import matplotlib.image as mpimg
# Import everything needed to edit/save/watch video clips
#from moviepy.editor import VideoFileClip


def set_max(value, min_value, max_value):
  if value > 0 and value > max_value:
      return max_value
  if value < 0 and value < min_value:
      return min_value
  return value


os.chdir(r'/home/thiago/Documentos/TCC/Sato')
vrep.simxFinish(-1) # just in case, close all opened connections
clientID=vrep.simxStart('127.0.0.1',19999,True,True,5000,5) # Connect to V-REP

ErrorCode, steeringLeft = vrep.simxGetObjectHandle(clientID,'nakedCar_steeringLeft',vrep.simx_opmode_oneshot_wait)
ErrorCode, steeringRight = vrep.simxGetObjectHandle(clientID,'nakedCar_steeringRight',vrep.simx_opmode_oneshot_wait)
ErrorCode, motorLeft = vrep.simxGetObjectHandle(clientID,'nakedCar_motorLeft',vrep.simx_opmode_oneshot_wait)
ErrorCode, motorRight = vrep.simxGetObjectHandle(clientID,'nakedCar_motorRight',vrep.simx_opmode_oneshot_wait)
ErrorCode, vision_sensor = vrep.simxGetObjectHandle(clientID,'Vision_sensor',vrep.simx_opmode_oneshot_wait)
ErrorCode, leftdis = vrep.simxGetDistanceHandle(clientID,'left_dist',vrep.simx_opmode_oneshot_wait)
ErrorCode, rightdis = vrep.simxGetDistanceHandle(clientID,'right_dist',vrep.simx_opmode_oneshot_wait)
ErrorCode, car_size = vrep.simxGetDistanceHandle(clientID,'car_size',vrep.simx_opmode_oneshot_wait)
ErrorCode, disL = vrep.simxReadDistance(clientID,leftdis,vrep.simx_opmode_streaming)
ErrorCode, disR = vrep.simxReadDistance(clientID,rightdis,vrep.simx_opmode_streaming)
desiredWheelRotSpeed = 5

vrep.simxSetJointTargetVelocity(clientID,motorLeft,desiredWheelRotSpeed,vrep.simx_opmode_streaming)
vrep.simxSetJointTargetVelocity(clientID,motorRight,desiredWheelRotSpeed,vrep.simx_opmode_streaming)

d = 0.53
l = 0.68
r = 0.15

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

j = 0
k = 1

# list for data aquisition
t = []
m_center = []
path_size = []
path_l = []
path_r = []
velocity = []
for i in range(100000):
    # Read sensor values for prior analysis
    ErrorCode, disL = vrep.simxReadDistance(clientID,leftdis,vrep.simx_opmode_buffer)
    ErrorCode, disR = vrep.simxReadDistance(clientID,rightdis,vrep.simx_opmode_buffer)
    ErrorCode, lt = vrep.simxReadDistance(clientID,car_size,vrep.simx_opmode_buffer)
    
    # Receives the image from v-rep
    res,resolution,image = vrep.simxGetVisionSensorImage(clientID,vision_sensor,0,vrep.simx_opmode_buffer)
    img = np.array(image, dtype = np.uint8)
    img.resize([resolution[0], resolution[1], 3])
    img = np.rot90(img,2)
    img = np.fliplr(img)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    img = img[50:255,:]
    
    # Store values for prior analysis
    dt = lt + disL + disR
    path_size.append(dt)
    path_l.append(-dt/2)
    path_r.append(dt/2)
    measure_center = (disL+(dt-disR))/2 - dt/2
    t.append(i*0.1)
    m_center.append(measure_center)
    print ("Center: " + str(measure_center));
    
    
    try:
        # image processing
        video = img
        video_street = lane_detector(img)
        #video_street[video_street == 1] = 255
      
        #cv2.imshow('Image 2', video_street)
        #tecla = cv2.waitKey(10) & 0xFF
        #if tecla == 27: 
        #    break
          
        #video_street[video_street == 255] = 1
        
        try:
          left_fit, right_fit, video_shape = fit_lines(video_street)
          left_cur, right_cur, left_x, right_x, distance_center = curvature(left_fit, right_fit, video_shape)
          video_road = draw_lines(video, left_x, right_x)
          curv = (left_cur + right_cur) / 2.0
          add_text_to_image(video_road, curv, distance_center)
          curv_max = curv
          dist_center_max = distance_center
          # curv_max = set_max(curv, -200.0, 200.0)
          # dist_center_max = set_max(distance_center, -0.5, 0.5)
        except Exception as e:
          video_road = video
          dist_center_max = 0
          curv_max = 0
          
        center = dist_center_max
        curve = curv_max
        
        # Show image in an external window
        cv2.imshow('Image', video_road)
        tecla = cv2.waitKey(10) & 0xFF
        if tecla == 27: 
            break
    
        # control constant
        # k1 = 250.0
        k1 = 6.0
        control = k1*center
        if abs(control)>0.45:
            print ("---");
            desiredSteeringAngle = (control)*0.45/abs(control)
        else:   
            desiredSteeringAngle = control
        
        desiredSteeringAngle = -desiredSteeringAngle
        
        if abs(desiredSteeringAngle) > 0.45:
            desiredSteeringAngle = 0.45*desiredSteeringAngle/abs(desiredSteeringAngle)
        if desiredSteeringAngle > 0:
            steeringAngleLeft = math.atan(l/(-d+l/math.tan(desiredSteeringAngle)))
            steeringAngleRight = math.atan(l/(d+l/math.tan(desiredSteeringAngle)))
        else:
            steeringAngleRight = -math.tan(l/(-d+l/math.tan(-desiredSteeringAngle)))
            steeringAngleLeft = -math.atan(l/(d+l/math.tan(-desiredSteeringAngle)))


        desiredWheelRotSpeed = 10
        vel = desiredWheelRotSpeed*r*3.6
        velocity.append(vel)
        
        # Send to v-rep the output from control
        vrep.simxSetJointTargetPosition(clientID,steeringLeft,steeringAngleLeft,vrep.simx_opmode_streaming)
        vrep.simxSetJointTargetPosition(clientID,steeringRight,steeringAngleRight,vrep.simx_opmode_streaming)
        vrep.simxSetJointTargetVelocity(clientID,motorLeft,desiredWheelRotSpeed,vrep.simx_opmode_streaming)
        vrep.simxSetJointTargetVelocity(clientID,motorRight,desiredWheelRotSpeed,vrep.simx_opmode_streaming)
        k = 1
    except Exception as e:
        k = k + 1
        print (e);
        print ("Image processing FAILED");
        if k == 4:
            vrep.simxPauseSimulation(clientID,vrep.simx_opmode_oneshot)

    
    time.sleep(0.1)
    
cv2.destroyAllWindows()

# Plot the curves for prior analysis

plt.plot(t,m_center)
plt.axis([5, t[-1], -0.5, 0.5])
plt.xlabel('Time (s)')
plt.ylabel('Distance (m)')
plt.show()

np.std(m_center)

plt.plot(t,velocity)
plt.axis([0, t[-1], 5, 11])
plt.xlabel('Time (s)')
plt.ylabel('Velocity (m/s)')
plt.show()