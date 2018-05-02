# Blurring and Sharpening Images

# Import Computer Vision package - cv2
import cv2

# Import Numerical Python package - numpy as np
import numpy as np

# Read the image using imread built-in function
image = cv2.imread('image_6.jpg')

# Display original image using imshow built-in function
cv2.imshow("Original", image)

# Wait until any key is pressed
cv2.waitKey(0)

# Blurring images: Averaging, cv2.blur built-in function
# Averaging: Convolving image with normalized box filter
# Convolution: Mathematical operation on 2 functions which produces third function.
# Normalized box filter having size 3 x 3 would be:
# (1/9)  [[1, 1, 1],
#		 [1, 1, 1],
# 		 [1, 1, 1]]
blur = cv2.blur(image,(9,9)) # (9 x 9) filter is used 

# Display blurred image
cv2.imshow('Blurred', blur)

# Wait until any key is pressed
cv2.waitKey(0)

# Sharpening images: Emphasizes edges in an image

kernel = np.array([[-1,-1,-1], 
                   [-1,9,-1], 
                   [-1,-1,-1]])
# If we don't normalize to 1, image would be brighter or darker respectively    
                          
# cv2.filter2D is the built-in function used for sharpening images
# cv2.filter2D(image, ddepth, kernel)
sharpened = cv2.filter2D(image, -1, kernel)
# ddepth = -1, sharpened images will have same depth as original image

# Display sharpenend image
cv2.imshow('Sharpened', sharpened)

# Wait untill any key is pressed
cv2.waitKey(0)

# Close all windows
cv2.destroyAllWindows()
