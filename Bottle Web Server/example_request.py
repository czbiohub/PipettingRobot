import requests
from opentrons import robot
import time

serveradress = 'localhost:8080/'
def camerarequest(step):
    # Send a GET request to serveradress/step until a 'done' is returned.
    done = False
    while not done:
        r = requests.get(serveradress + "update/"  + step)
        done = r.json()['done']

def temprequest(device, command, mode):
    # Available devices: 1 or 2.

    # Available Commands for tempdecks:
    # M104-Sn --> n = desired temperature in degrees celsius between 4 and 94 degrees
    # M105 --> Get temperature from tempdeck. Will return in server console on host computer.
    # M18 --> Turn off tempdeck.

    # Available modes: "wait" or "proceed". Wait will return done once set temperature has been reached, anything else will set a temperature and return done instantly.
    # done = False
    # while not done:
    if not robot.is_simulating(): # A simulation check is ran whenever a temprequest is used in a protocol. This is due to the fact that a protocol is ran every time it uploads to the OT-2, and when that happens you'd usually not want eny external equipment to start capturing images or changing temps.
        commandinfo = str(device) + "_" + command + "_" + mode #device id 1 or 2, GCode command, wait or don't wait mode.
        r = requests.get(serveradress + "tempdeck/" + commandinfo)
        returnmsg = r.text
        print(returnmsg)
        robot.comment(returnmsg)
    else:
        return 'robot is simulating, no temperature set.'

camerarequest('capture_image') # capture a single frame

time.sleep(3)

camerarequest('toggle_video') # toggle on video capture script on server

temprequest(1,'M104-S25', 'wait')

temprequest(2,'M104-S50', 'proceed')

camerarequest('toggle_video') # toggle off video capture script on server