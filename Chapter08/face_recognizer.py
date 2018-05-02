import os
import cv2
import numpy as np
from sklearn import preprocessing

# Class to handle tasks related to label encoding
class LabelEncoding(object):
    # Method to encode labels from words to numbers
    def encoding_labels(self, label_wordings):
        self.le = preprocessing.LabelEncoder()
        self.le.fit(label_wordings)

    # Convert input label from word to number
    def word_to_number(self, label_wordings):
        return int(self.le.transform([label_wordings])[0])

    # Convert input label from number to word
    def number_to_word(self, label_number):
        return self.le.inverse_transform([label_number])[0]

# Extract images and labels from input path
def getting_images_and_labels(path_input):
    label_wordings = []

    # Iterate through the input path and append files
    for roots, dirs, files in os.walk(path_input):
        for fname in (x for x in files if x.endswith('.jpg')):
            fpath = os.path.join(roots, fname)
            label_wordings.append(fpath.split('/')[-2]) 
            
    # Initialize variables
    images = []
    le = LabelEncoding()
    le.encoding_labels(label_wordings)
    labels = []

    # Parse the input directory
    for roots, dirs, files in os.walk(path_input):
        for fname in (x for x in files if x.endswith('.jpg')):
            fpath = os.path.join(roots, fname)

            # Read the image in grayscale format
            img = cv2.imread(fpath, 0) 

            # Extract the label
            names = fpath.split('/')[-2]
                
            # Perform face detection
            face = faceCascade.detectMultiScale(img, 1.1, 2, minSize=(100,100))

            # Iterate through face rectangles
            for (x, y, w, h) in face:
                images.append(img[y:y+h, x:x+w])
                labels.append(le.word_to_number(names))

    return images, labels, le

if __name__=='__main__':
    path_cascade = "haarcascade_frontalface_alt.xml"
    train_img_path = 'faces_dataset/train'
    path_img_test = 'faces_dataset/test'

    # Load face cascade file
    faceCascade = cv2.CascadeClassifier(path_cascade)

    # Initialize Local Binary Patterns Histogram face recognizer
    face_recognizer = cv2.createLBPHFaceRecognizer()

    # Extract images, labels, and label encoder from training dataset
    imgs, labels, le = getting_images_and_labels(train_img_path)

    # Train the face recognizer 
    print "\nTraining..."
    face_recognizer.train(imgs, np.array(labels))

    # Test the recognizer on unknown images
    print '\nPerforming prediction on test images...'
    flag_stop = False
    for roots, dirs, files in os.walk(path_img_test):
        for fname in (x for x in files if x.endswith('.jpg')):
            fpath = os.path.join(roots, fname)

            # Read the image
            predicting_img = cv2.imread(fpath, 0)

            # Detect faces
            face = faceCascade.detectMultiScale(predicting_img, 1.1, 
                    2, minSize=(100,100))

            # Iterate through face rectangles
            for (x, y, w, h) in face:
                # Predict the output
                index_predicted, config = face_recognizer.predict(
                        predicting_img[y:y+h, x:x+w])

                # Convert to word label
                person_predicted = le.number_to_word(index_predicted)

                # Overlay text on the output image and display it
                cv2.putText(predicting_img, 'Prediction: ' +  person_predicted, 
                        (10,60), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 6)
                cv2.imshow("Recognizing face", predicting_img)

            a = cv2.waitKey(0)
            if a == 27:
                flag = True
                break

        if flag_stop:
            break

