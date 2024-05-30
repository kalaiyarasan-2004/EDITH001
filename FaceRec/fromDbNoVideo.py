import cv2
import face_recognition
import sqlite3
import numpy as np

# Connect to SQLite database
conn = sqlite3.connect('Database/face_recognition.db')
c = conn.cursor()

# Load known faces from the database
c.execute("SELECT name, encoding FROM known_faces")
known_faces = c.fetchall()
conn.close()

known_face_encodings = [np.frombuffer(encoding, dtype=np.float64) for name, encoding in known_faces]
known_face_names = [name for name, encoding in known_faces]

# Initialize the webcam video capture
video_capture = cv2.VideoCapture(0)

# Flag to check if the person is recognized
recognized_person = None

while True:
    # Capture a single frame of video
    ret, frame = video_capture.read()

    # Resize frame for faster processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (OpenCV) to RGB color (face_recognition)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Find all the faces and face encodings in the current frame of video
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    # Loop through each face found in the frame
    for face_encoding, face_location in zip(face_encodings, face_locations):
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"

        # Use the known face with the smallest distance to the new face
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = face_distances.argmin()
        if matches[best_match_index]:
            name = known_face_names[best_match_index]

        # If a new person is recognized, print the name
        if recognized_person != name and name != "Unknown":
            recognized_person = name
            print(f"Detected: {name}")

        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top, right, bottom, left = face_location
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        #
