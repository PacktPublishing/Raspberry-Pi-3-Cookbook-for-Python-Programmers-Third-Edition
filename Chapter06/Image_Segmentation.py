# Image Segmatation using Contours
# Segmentation: Partitioning images into different regions
# Contours: Lines or curves around the boundary of an object

# Import Computer Vision package - cv2
import cv2

# Import Numerical Python package - numpy as np
import numpy as np

# Read the image using imread built-in function
image = cv2.imread('image_5.jpg')

# Display original image using imshow built-in function
cv2.imshow("Original", image)

# Wait until any key is pressed
cv2.waitKey(0)

# cv2.Canny is the built-in function used to detect edges
# cv2.Canny(image, threshold_1, threshold_2)
canny = cv2.Canny(image, 50, 200)

# Display edge detected output image using imshow built-in function
cv2.imshow("Canny Edge Detection", canny)

# Wait until any key is pressed
cv2.waitKey(0)

# cv2.findContours is the built-in function to find contours
# cv2.findContours(canny, contour retrieval mode, contour approximation mode)
# contour retrieval mode: cv2.RETR_LIST (retrieves all contours) 
# contour approximation mode: cv2.CHAIN_APPROX_NONE (stores all boundary points)
contours, hierarchy = cv2.findContours(canny, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

# cv2.drawContours is the the built-in function to draw contours
# cv2.drawContours(image, contours, index of contours, color, thickness)
cv2.drawContours(image, contours, -1, (255,0,0), 10)
# index of contours = -1 will draw all the contours

# Display contours using imshow built-in function
cv2.imshow("Contours", image)

# Wait until any key is pressed
cv2.waitKey()

# Close all windows
cv2.destroyAllWindows()
