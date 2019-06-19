# This script is written for being run by server.py, NOT directly by a user.
# Usage: This script is executed as a subprocess by the server.py program. This is done so that a video capture stream can be started and ran in parallell with the server script.
import cv2
import numpy as np
import datetime
import os

cap = cv2.VideoCapture(1) # Create a video capture device using camera device id VideoCapture(id). This number can be found by running the command 'ls /dev/ttyACM*' in a terminal window on Linux or Mac. This will give you a list of all devices using the ttyACM* name, unplug and replug your camera while repeating the command to identify the right id.

def videocapture(): # Captures a frame every 200ms (= 5 FPS stream), saving the captured frames with date in a timestamped folder of the start time. Will also show a window giving the user a real-time view of the captures.
    starttime = str(datetime.datetime.now()).replace(" ", "_")
    path = r"./Captured Runs/captures_" + str(starttime).replace(":", "")
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