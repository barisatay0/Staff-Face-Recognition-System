import cv2
import numpy as np
import os
import pandas as pd
import datetime

# Load data folder and tags
data_folder = "Data"
labels = os.listdir(data_folder)
last_update_times = {} # To follow Staff latest update times
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Loading the facial recognition model
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("trained_model.yml")

# Load staff data
staffs_df = pd.read_excel("data.xlsx")
staffs_df["StaffId"] = staffs_df["StaffId"].astype(str) 

# Function that updates the staff "Check" column
def update_check(staff_id):
    matching_staffs = staffs_df[staffs_df["StaffId"] == staff_id]
    if not matching_staffs.empty:
        row_index = matching_staffs.index[0]
        current_check = staffs_df.at[row_index, "Check"]
        last_update_time = last_update_times.get(staff_id, None)
    # Check if 60 seconds have passed since the last update
        if last_update_time is None or (datetime.datetime.now() - last_update_time).total_seconds() >= 60:
            new_check = 1 if current_check == 0 else 0
            staffs_df.at[row_index, "Check"] = new_check
            last_update_times[staff_id] = datetime.datetime.now()
            print(f"StaffId {staff_id} Check is update: {new_check}")
        else:
            pass # Do not update if 60 seconds have not passed
    else:
        print(f"Hata: {staff_id} Staff id was not found in the database.")

# Function that recognizes faces
def recognize_faces(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
    for (x, y, w, h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        label_id, confidence = recognizer.predict(roi_gray)
        if confidence < 40:
            staff_id = labels[label_id]
            match_text = "Match!"
            update_check(staff_id)
        else:
            staff_id = "Unknown!"
            match_text = ""
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        cv2.putText(frame, f"{staff_id} ({int(confidence)})", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
        if match_text:
            cv2.putText(frame, match_text, (x, y-40), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    return frame

# Main function
def main():
    cap = cv2.VideoCapture(0)
    cv2.namedWindow('Face Recognition', cv2.WINDOW_GUI_NORMAL)
    cv2.resizeWindow('Face Recognition', 800, 600) 
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = recognize_faces(frame)
        cv2.imshow('Face Recognition', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

    # Save staff data as updated
    staffs_df.to_excel("data.xlsx", index=False)

if __name__ == "__main__":
    main()
