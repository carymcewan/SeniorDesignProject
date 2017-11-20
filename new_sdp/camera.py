
import cv2
import numpy as np
from picamera import PiCamera


class CameraDisconnected(Exception):
    def __init__(self):
        Exception.__init__(self, "Camera Not Connected")


class Camera:
    def __init__(self):
        self._camera = None

        self.brightness = 0
        self.contrast = 0
        self.saturation = 0
        self.exposure = 0
        self._shutter_speed = 0

        self._width = 0
        self._height = 0
        self._resolution = (self._width, self._height)

        self._image_shape = np.empty((self._width * self._height * 3,), dtype=np.uint8)
        self._last_image = None

    def set_brightness(self, value):
        self.brightness = value

    def set_contrast(self, value):
        self.contrast = value

    def set_saturation(self, value):
        self.saturation = value

    def set_exposure(self, value):
        self.exposure = value

    def set_shutter_speed(self, value):
        self._shutter_speed = value

    def set_resolution(self, width, height):
        self._width = width
        self._height = height
        self._resolution = (width, height)
        self._image_shape = np.empty((self._width * self._height * 3,), dtype=np.uint8)

    def initialize(self, shutter_speed, height, width):
        self._camera = PiCamera()
        self._camera.shutter_speed = shutter_speed
        self._height = height
        self._width = width

    def capture_image(self):
        self._camera.capture(self._image_shape, 'bgr')
        self._last_image = self._image_shape.reshape((self._width, self._height, 3))
        return cv2.cvtColor(self._last_image, cv2.COLOR_BGR2RGB)

    def save_image(self, filename):
        image = cv2.cvtColor(self._last_image, cv2.COLOR_RGB2BGR)
        cv2.imwrite(filename, image)

def vflip_image(image):
    return cv2.flip(image, 0)

def hflip_image(image):
    return cv2.flip(image, 1)
