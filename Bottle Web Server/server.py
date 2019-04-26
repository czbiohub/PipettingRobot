import cv2
from bottle import route, run
import subprocess
import os
import signal
import datetime
import serial
import time

videocapturepath = os.path.realpath(r"./Bottle Web Server/videocapture.py")
commands = ['python', videocapturepath]
global capturing
capturing = False

@route('/update/<step>')
def update(step):
	global capturing
	if step == "toggle_video":
		if capturing == False:
			capturing = True
			global proc
			proc = subprocess.Popen(commands, shell= False)
		else:
			subprocess.call('kill ' + str(proc.pid), shell = True)
			capturing = False
		return {"done" : "jsonData"}

	if step == "capture_image":
		if capturing == True:
			return {"already_capturing" : "jsonData"}
		else:
			cap = cv2.VideoCapture(0)
			starttime = datetime.datetime.now()
			path = "./captures_" + str(starttime).replace(":", "")
			os.mkdir(path)
			status, frame = cap.read()
			if status == True:
				frame = frame[371:490,588:699,:]            
				now = datetime.datetime.now()
				cv2.imwrite(path + "/capture_" + str(now).replace(":", "").replace(" ", "_") + ".jpg", frame)
				cap.release()
				cv2.destroyAllWindows()
				return {"done" : "jsonData"}

@route('/tempdeck/<commandinfo>')
def tempdeck(commandinfo):
	commandinfo = commandinfo.split("_")
	print("Recieved device ID: " + commandinfo[0])
	print("Recieved command: " + commandinfo[1])
	print("Recieved mode: " + commandinfo[2])
	print("\n")

	# Device ID checks and assignment to adresses
	if commandinfo[0] == "1":
		tempdeck = serial.Serial('/dev/ttyACM0', baudrate=115200, timeout = 0.5)
	elif commandinfo[0] == "2":
		tempdeck = serial.Serial('/dev/ttyACM0', baudrate=115200, timeout = 0.5)
	else:
		print("No valid device ID provided. Double check that attached devices are associated with the correct adresses")
		return {"Device ID incorrect, no command was sent to tempdeck." : "jsonData"}
	
	def tempdeckWrite(writecommand):
		tempdeck.write(str.encode(writecommand))
		time.sleep(0.1)
		response = tempdeck.read_all().decode()
		print("GCode command " + repr(writecommand) + " was sent to tempdeck " + commandinfo[0] + ". Response: " + repr(response))
		return response

	# Replace - in command (e.g M104-S50) with space(s) and add endline before sending to tempdeck
	commandinfo[1] = (commandinfo[1].replace("-", " ")) + "\r\n" 
	tempdeckWrite(commandinfo[1])	

	# If the mode variable is set to wait, compare current temperature to set temperature until they are equal, and return done
	# Output from reading M105 command (get current and set temperature): Incoming format: T:30.000 C:23.088\r\nok\r\nok\r\n
	if commandinfo[2] == "wait":
		temps = tempdeckWrite("M105\r\n").split(" ")
		print("Temps response: " + repr(str(temps)))
		temps[1] = temps[1][0:8]
		print("Temps response after rstrip: " + repr(str(temps)))
		_, settemp = temps[0].split(":")
		print("Set temperature is: " + repr(settemp))
		_, currenttemp = temps[1].split(":")
		print("Current temperature is: " + repr(currenttemp))

		while (float(currenttemp) < (float(settemp) - 1)) or (float(currenttemp) > (float(settemp) + 1)):
			time.sleep(20)
			temps = tempdeckWrite("M105\r\n").split(" ") # Send M105 get temperature command
			print("(Inner) Temps response: " + repr(temps))
			temps[1] = temps[1][0:8]
			# print("Inner temps response after rstrip: " + repr(str(temps)))
			_ , settemp = temps[0].split(":")
			print("Set temperature is: " + settemp)
			_ , currenttemp = temps[1].split(":")
			print("Current temperature is: " + currenttemp)
		returnmsg = "Temperature has reached " + currenttemp + "°C on tempdeck " + commandinfo[0] + " proceeding with protocol..."
		tempdeck.close()
		return returnmsg
	else:
		tempdeck.close()
		returnmsg = None
		return returnmsg

run(host='0.0.0.0', port = 8080, debug=True) #0.0.0.0 = Listen to all interfaces