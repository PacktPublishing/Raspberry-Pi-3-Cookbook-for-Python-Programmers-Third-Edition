# Erosion and Dilation are Morphological Operations
# Erosion: Removes pixels at the boundaries of objects in an image
# Dilation: Adds pixels to the boundaries of objects in an image

# Import Computer Vision package - cv2
import cv2

# Import Numerical Python package - numpy as np
import numpy as np

# Read the image using imread built-in function
image = cv2.imread('image_4.jpg')

# Display original image using imshow built-in function
cv2.imshow("Original", image)

# Wait until any key is pressed
cv2.waitKey(0)

# np.ones returns an array, given shape and type, filled with ones
# np.ones(shape, dtype)
kernel = np.ones((5,5), dtype = "uint8")
# 5 x 5 is the dimension of the kernal
# uint8: is an unsigned integer (0 to 255)

# cv2.erode is the built-in function used for erosion
# cv2.erode(image, kernel, iterations)
erosion = cv2.erode(image, kernel, iterations = 1)

# Display image after erosion using imshow built-in function
cv2.imshow("Erosion", erosion)

# Wait until any key is pressed
cv2.waitKey(0)

# cv2.dilate is the built-in function used for dilation
# cv2.dilate(image, kernel, iterations)
dilation = cv2.dilate(image, kernel, iterations = 1)

# Display image after dilation using imshow built-in function
cv2.imshow("Dilation", dilation)

# Wait until any key is pressed
cv2.waitKey(0)

# Close all windows
cv2.destroyAllWindows()
