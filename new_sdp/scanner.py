import queue
import time
import datetime
import numpy as np
from calibrator import Calibrator
from camera import Camera

PI2 = np.pi * 2.0
THETA = np.pi / 200.0

def scan():


def calculate_2d_points():






class Scanner:
    def __init__(self):
        self.image = None
        self.motor_step = 0
        self.theta = 0
        self.is_scanning = False
        self.camera = Camera()

    def set_motor_step(self, value):
        self.motor_step = value

    def initialize(self, camera):
        self.image = None
        self.theta = 0
        self.is_scanning = False
        self.camera = camera

    def _increment_theta(self):
        self.theta += self.theta


    def scan(self):
        cmat, dist_ceofs, \
        rmat, tmat, _ = Calibrator().calibration_data.load_calibrations()



    def differential_scan(self):
        cmat, dist_ceofs, \
        rmat, tmat, _ = Calibrator().calibration_data.load_calibrations()
        while self.is_scanning:
            if np.abs(self.theta) >= PI2:
                break
            else:
                begin = time.time()
                try:
                    image = self.camera.capture_image()


    def compute_2d_points(self, image):
        """ Uses segmented gaussian filter"""



if __name__ == "__main__":
    camera = Camera()
    camera.initialize(10000, 1920, 1080)

    scanner = Scanner()
    scanner.initialize(camera)

    scanner.scan()