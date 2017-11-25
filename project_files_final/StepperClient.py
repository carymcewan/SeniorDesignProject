import RPi.GPIO as gpio
import time

class StepperClient():
    def __init__(self, direction):
        # Define GPIO's
        self.directionPin = 23
        self.stepPin = 24
        gpio.setmode(gpio.BCM)
        gpio.setup(self.directionPin, gpio.OUT) # Direction
        gpio.setup(self.stepPin, gpio.OUT) # Step

        # Set direction of rotation
        if direction == 'left':
            gpio.output(self.directionPin, True)
        elif direction == 'right':
            gpio.output(self.directionPin, False)

    def step(self):
        gpio.output(self.stepPin, True)
        gpio.output(self.stepPin, False)

    def close(self):
        gpio.cleanup()
            
            
        
