import os
import sys

import cv2
import numpy as np

# Load input data 
in_file = 'words.data' 

# Define visualization parameters 
scale_factor = 10
s_index = 6
e_index = -1
h, w = 16, 8

# Loop until you encounter the Esc key
with open(in_file, 'r') as f:
    for line in f.readlines():
        information = np.array([255*float(x) for x in line.split('\t')[s_index:e_index]])
        image = np.reshape(information, (h,w))
        image_scaled = cv2.resize(image, None, fx=scale_factor, fy=scale_factor)
        cv2.imshow('Image', image_scaled)
        a = cv2.waitKey()
        if a == 10:
            break
