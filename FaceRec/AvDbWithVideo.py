import cv2
import dlib
import face_recognition
import numpy as np
import sqlite3

# Function to align faces using dlib's facial landmark detection
# Function to align faces using dlib's facial landmark detection
def align_face(image, face_locations):
    aligned_faces = []
    for face_location in face_locations:
        if isinstance(face_location, dlib.rectangle):  # Check if it's a single face detection
            top, right, bottom, left = face_location.top(), face_location.right(), face_location.bottom(), face_location.left()
            face = image[top:bottom, left:right]
            
            # Find facial landmarks
            shape_predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
            landmarks = shape_predictor(image, dlib.rectangle(left=left, top=top, right=right, bottom=bottom))
            
            # Align face using landmarks
            aligned_face = dlib.get_face_chip(image, landmarks, size=256)
            aligned_faces.append(aligned_face)
        else:  # Handle multiple face detections
            aligned_faces.extend([align_face(image, [loc])[0] for loc in face_locations])
    return aligned_faces


# Connect to SQLite database and load known faces
conn = sqlite3.connect('Database/face_recognition.db')
c = conn.cursor()
c.execute("SELECT name, encoding FROM known_faces")
known_faces = c.fetchall()
known_face_encodings = [np.frombuffer(encoding, dtype=np.float64) for _, encoding in known_faces]
known_face_names = [name for name, _ in known_faces]
conn.close()

# Initialize webcam and face detector
video_capture = cv2.VideoCapture(0)
face_detector = dlib.get_frontal_face_detector()

recognized_persons = set()

while True:
    ret, frame = video_capture.read()
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Detect faces using dlib
    face_locations = face_detector(rgb_small_frame, 1)

    # Align faces using landmarks
    aligned_faces = align_face(rgb_small_frame, face_locations)

    # Encode aligned faces
    face_encodings = [face_recognition.face_encodings(face)[0] for face in aligned_faces]

    for face_encoding, face_location in zip(face_encodings, face_locations):
        # Compare face encoding with known faces
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"
        if True in matches:
            name = known_face_names[matches.index(True)]

        if name != "Unknown" and name not in recognized_persons:
            recognized_persons.add(name)
            print(f"Detected: {name}")

        top, right, bottom, left = face_location.top(), face_location.right(), face_location.bottom(), face_location.left()
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
