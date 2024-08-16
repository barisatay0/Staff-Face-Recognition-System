import cv2
import os
import numpy as np

# Folder containing training data
data_folder = "Data"
labels = os.listdir(data_folder)

# OpenCV's facial recognition model
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Training data creation function
def create_training_data():
    training_data = []
    for label in labels:
        label_path = os.path.join(data_folder, label)
        for img_name in os.listdir(label_path):
            img_path = os.path.join(label_path, img_name)
            img = cv2.imread(img_path)
            if img is None:
                print(f"Warning: Could not read image {img_path}. Skipping.")
                continue
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
            for (x, y, w, h) in faces:
                roi_gray = gray[y:y+h, x:x+w]
                training_data.append([roi_gray, labels.index(label)])
    return training_data

# Generate training data
training_data = create_training_data()

# Check if there is training data
if not training_data:
    print("Error: No training data found. Please check your data folder and image files.")
else:
# Create LBPH face recognition model
    recognizer = cv2.face.LBPHFaceRecognizer_create()

    X = []  # Features
    y = []  # Tags
    for features, label in training_data:
        X.append(features)
        y.append(label)
    
    # Train the model
    recognizer.train(X, np.array(y))

    # Save trained model    
    recognizer.save("trained_model.yml")

    print("Model Trained Successfully.")
