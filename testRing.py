import config as c
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(c.RING_OUT, GPIO.OUT)

try:
	while True:
		time.sleep(0.2)
		print("On")
		GPIO.output(c.RING_OUT, True)
		time.sleep(0.2)
		print("off")
		GPIO.output(c.RING_OUT, False)
except:
	GPIO.output(c.RING_OUT, False)
	GPIO.cleanup()
