import time
import RPi.GPIO as gpio

gpio.setmode(gpio.BCM)
gpio.setup(17, gpio.OUT)
gpio.setup(27, gpio.OUT)
gpio.setup(22, gpio.OUT)

sleep = 0.1

gpio.output(17, False)
gpio.output(27, False)
gpio.output(22, False)

for i in range(4):
	gpio.output(17, True)
	time.sleep(sleep)
	gpio.output(27, True)
	time.sleep(sleep)
	gpio.output(22, True)

	time.sleep(sleep)
	gpio.output(17, False)
	time.sleep(sleep)
	gpio.output(27, False)
	time.sleep(sleep)
	gpio.output(22, False)

	time.sleep(sleep)

gpio.output(17, True)
gpio.output(27, True)
gpio.output(22, True)

time.sleep(0.5)

sleep2 = 0.25
gpio.output(22, False)
time.sleep(sleep2)

gpio.output(27, False)
time.sleep(sleep2)

gpio.output(17, False)
time.sleep(sleep2)

gpio.output(17, True)

time.sleep(sleep2*4)
gpio.output(17, False)

gpio.cleanup()