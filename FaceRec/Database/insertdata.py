import face_recognition
import os
import sqlite3
import numpy as np

known_faces_dir = "facedata"  # Replace with your actual path

# Connect to SQLite database
conn = sqlite3.connect('Database/face_recognition.db')
c = conn.cursor()

# Load and encode known faces
for filename in os.listdir(known_faces_dir):
    if filename.endswith((".jpg", ".jpeg", ".png")):
        path = os.path.join(known_faces_dir, filename)
        image = face_recognition.load_image_file(path)
        encodings = face_recognition.face_encodings(image)
        if encodings:  # Ensure there's at least one face found
            encoding = encodings[0]
            name = os.path.splitext(filename)[0]
            c.execute("INSERT INTO known_faces (name, encoding) VALUES (?, ?)",
                      (name, encoding.tobytes()))

conn.commit()
conn.close()
