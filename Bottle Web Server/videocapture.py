import cv2
import numpy as np
import datetime
import os

cap = cv2.VideoCapture(1)

def videocapture():
    starttime = str(datetime.datetime.now()).replace(" ", "_")
    path = "./captures_" + str(starttime).replace(":", "")
    os.mkdir(path)
    while cap.isOpened(): 
        status, frame = cap.read()
        if status == True:
            # Display the resulting frame
            # frame = frame[245:300,295:345,:]
            cv2.imshow('Frame',frame)            
            now = str(datetime.datetime.now()).replace(" ", "_")
            if cv2.waitKey(200):
                cv2.imwrite(path + "/capture_" + str(now).replace(":", "") + ".jpg", frame)
        else: 
            cap.release()
            cv2.destroyAllWindows()
            break

videocapture()