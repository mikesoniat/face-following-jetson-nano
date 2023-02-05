# AI Face Following with Jetson Nano
# Using OpenCV and Harr Cascade Classifier
# Mike Soniat
# 2022

import time 
import cv2
from adafruit_servokit import ServoKit

# vars
dispW=640
dispH=480
flip=0
panServo = 0
tiltServo = 1
pan = 90
tilt = 120

#add web cam
cam = cv2.VideoCapture(1)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, dispW)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, dispH)

#add servos
kit = ServoKit(channels=16)
kit.servo[panServo].angle = pan
kit.servo[tiltServo].angle = tilt 

#import models
face_cascade = cv2.CascadeClassifier('/home/mikes/Desktop/PyPro/cascade/face.xml')
eye_cascade = cv2.CascadeClassifier('/home/mikes/Desktop/PyPro/cascade/eye.xml')

while True:
    ret, frame = cam.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3,5)

    for (x,y,w,h) in faces:
        cv2.rectangle(frame, (x,y), (x+w,y+h), (0,0,255), 2)

        if True:
            objX = x+w/2
            objY = y+h/2
            errorPan = objX-dispW/2
            errorTilt = objY-dispH/2

            if abs(errorPan) > 15:
                pan = pan - errorPan/75
            if abs(errorTilt) > 15:
                tilt = tilt - errorTilt/75

            #fix out of range errors
            if pan > 180:
                pan = 180
                print("Pan Out of Range")
            if pan < 0:
                pan = 0
                print("Pan Out of Range")
            if tilt > 180:
                tilt = 180
                print("Tilt Out of Range")
            if tilt < 0:
                tilt = 0
                print("Tilt Out of Range")

            kit.servo[panServo].angle = pan
            kit.servo[tiltServo].angle = tilt

            print("coordinates ", int(pan), ',', int(tilt))

            #create a region of interest
            roi_gray = gray[y:y+h,x:x+w]
            roi_color = frame[y:y+h,x:x+w]
            eyes = eye_cascade.detectMultiScale(roi_gray)
            for (xEye, yEye, wEye, hEye) in eyes:
                cv2.rectangle(roi_color, (xEye,yEye), (xEye+wEye,yEye+hEye), (255,0,0), 2)
                #cv2.circle(roi_color, (int(xEye+wEye/2), int(yEye+hEye/2)), 16, (255,0,0), 1)

            break 

    cv2.imshow('nanoCam',frame)
    cv2.moveWindow('nanoCam', 1000,50)
    if cv2.waitKey(1)==ord('q'):
        pan = 90
        tilt = 120
        time.sleep(1)
        kit.servo[panServo].angle = pan
        kit.servo[tiltServo].angle = tilt 

        break
cam.release()
cv2.destroyAllWindows()
