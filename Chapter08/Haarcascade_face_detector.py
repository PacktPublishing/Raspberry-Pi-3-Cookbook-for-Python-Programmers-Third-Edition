import cv2
import numpy as np

# Load face cascade file
frontalface_cascade= cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')

# Check if face cascade file has been loaded
if frontalface_cascade.empty():
	raise IOError('Unable to load the face cascade classifier xml file')

# Initialize video capture object
capture = cv2.VideoCapture(0)

# Define the scaling factor
scale_factor = 0.5

# Loop until you hit the Esc key
while True:
    # Capture current frame  and resize it
    ret, frame = capture.read()
    frame = cv2.resize(frame, None, fx=scale_factor, fy=scale_factor, 
            interpolation=cv2.INTER_AREA)

    # Convert to grayscale
    gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Run the face detector on the grayscale image
    face_rectangle = frontalface_cascade.detectMultiScale(gray_image, 1.3, 5)

    # Draw rectangles on the image
    for (x,y,w,h) in face_rectangle:
        cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 3)

    # Display the image
    	cv2.imshow('Face Detector', frame)

    # Check if Esc key has been pressed
    a = cv2.waitKey(1)
    if a == 10:
        break

# Release the video capture object and close all windows
capture.release()
cv2.destroyAllWindows()
