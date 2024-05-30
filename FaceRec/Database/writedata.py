import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('face_recognition.db')
c = conn.cursor()

# Create table for known faces
c.execute('''
CREATE TABLE IF NOT EXISTS known_faces (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    encoding BLOB NOT NULL
)
''')
conn.commit()
conn.close()
