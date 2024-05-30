import cv2
facemodal=cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
cam=cv2.VideoCapture(0)
while True:
    work,frame=cam.read()
    blackndwhite=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    face=facemodal.detectMultiScale(blackndwhite)
    for (x,y,w,h) in face:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)
    cv2.imshow("vid",frame)
    cv2.waitKey(1)
