from bottle import route, run
import pygame, pygame.camera
import datetime

pygame.camera.init()
pygame.camera.list_cameras()
cam = pygame.camera.Camera("/dev/video1", (1280, 1024)) # To find camera path (on linux): ls /dev/video*

@route('/update/<step>')  # Update route takes a step name through a GET request, adressed to http://any-ip-of-this-computer:8080/update/any-step-name 
def update(step):
	if step == "capture_image":	# If the request is with step capture_image, this server captures an image with the current datestamp and returns a 'done' to the requesting machine
		cam.start()
		now = datetime.datetime.now()
		img = cam.get_image()
		pygame.image.save(img,"capture " + str(now) + ".jpg")
		cam.stop()
		return {"done" : "jsonData"}
run(host='0.0.0.0', port = 8080, debug=True) #0.0.0.0 = Listen to all interfaces