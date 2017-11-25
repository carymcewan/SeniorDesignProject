import RPi.GPIO as gpio
import time

class LaserClient():
    def __init__(self, pin):

        # Define GPIO's
        self.laserPin = pin
        gpio.setmode(gpio.BCM)
        gpio.setup(self.laserPin, gpio.OUT)

    def turnOn(self):
        gpio.output(self.laserPin, True)

    def turnOff(self):
        gpio.output(self.laserPin, False)

    def toggle(self, delay):
        self.turnOn()
        time.sleep(delay)
        self.turnOff()
        
