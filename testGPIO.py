import config as c
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

##HANGUP_PIN GREEN_PIN
GPIO.setup(c.HANGUP_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP) #GPIO button
GPIO.setup(c.GREEN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
	while True:
		button_state_hangup = GPIO.input(c.HANGUP_PIN)
		button_state_green = GPIO.input(c.GREEN_PIN)
		if button_state_hangup == GPIO.LOW:
			print("Phone is Picked up")
		if button_state_green == GPIO.LOW:
			print("Green button press")
except:
	GPIO.cleanup()
