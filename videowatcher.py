import numpy as np
import cv2
import time

cap = cv2.VideoCapture('/home/pi/output.avi')

while(cap.isOpened()):
    ret, frame = cap.read()
    time.sleep(.2)

#    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break

cap.release()

