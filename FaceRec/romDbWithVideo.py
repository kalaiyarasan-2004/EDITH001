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

# Decode the encodings
known_face_encodings = [np.frombuffer(encoding, dtype=np.float64) for _, encoding in known_faces]
known_face_names = [name for name, _ in known_faces]

# Initialize the webcam video capture
video_capture = cv2.VideoCapture(0)

# Set to store names of recognized persons to ensure we print each name only once
recognized_persons = set()

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

        # If a new person is recognized and hasn't been recognized before, print the name
        if name != "Unknown" and name not in recognized_persons:
            recognized_persons.add(name)
            print(f"Detected: {name}")

        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top, right, bottom, left = face_location
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        # Draw a label with the name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting frame
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
