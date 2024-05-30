import cv2
import face_recognition

# Load the reference image and get the face encoding
picture_of_me = face_recognition.load_image_file("kalai.jpg")
my_face_encoding = face_recognition.face_encodings(picture_of_me)[0]

# Initialize the webcam video capture
video_capture = cv2.VideoCapture(0)

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
    for face_encoding in face_encodings:
        # See if the face is a match for the known face(s)
        results = face_recognition.compare_faces([my_face_encoding], face_encoding)

        if results[0] == True:
            print("It's a picture of me!")
        else:
            print("It's not a picture of me!")

    # Display the resulting image
    for (top, right, bottom, left) in face_locations:
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

    # Display the resulting frame
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
