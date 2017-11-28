from picamera import PiCamera
import time

camera = PiCamera()
camera.shutter_speed = 5000
camera.resolution = (1080, 1080)

time.sleep(3)

camera.capture('testing.jpg', use_video_port=True)
