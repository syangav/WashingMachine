import cv2
import send_email
import os
# Camera 0 is the integrated web cam on my netbook

 
#Number of frames to throw away while the camera adjusts to light levels
ramp_frames = 30
 
# Now we can initialize the camera capture object with the cv2.VideoCapture class.
# All it needs is the index to a camera port.
camera = cv2.VideoCapture(0)
 
# Captures a single image from the camera and returns it in PIL format
def get_image():
 # read is the easiest way to get a full image out of a VideoCapture object.
	retval, im = camera.read()
	return im
 

for i in xrange(ramp_frames):
	temp = get_image()
print("Taking image...")
# Take the actual image we want to keep
camera_capture = get_image()
file = "/home/ustone/debug/test_image.jpg"
# A nice feature of the imwrite method is that it will automatically choose the
# correct format based on the file extension you provide. Convenient!
try:
    os.remove(file)
except OSError:
    pass
cv2.imwrite(file, camera_capture)
print("Image is stored as ~/debug/test_image.jpg")

del(camera)
#send this image to debug.ust.one@gmail.com
send_email.send_email(file,'no ssocr output')
# You'll want to release the camera, otherwise you won't be able to create a new
# capture object until your script exits
