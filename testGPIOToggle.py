import config as c
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

##HANGUP_PIN GREEN_PIN
GPIO.setup(c.HANGUP_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP) #GPIO button
#GPIO.setup(c.HANGUP_PIN, GPIO.IN)
GPIO.setup(c.GREEN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

hangupState = GPIO.input(c.HANGUP_PIN)

def HANGUP_BTN_EVENT(channel):
	#state = GPIO.input(c.HANGUP_PIN)
	if hangupState == GPIO.LOW:
		print("Aufgelegt")
	else:
		print("Abgehoben")


GPIO.add_event_detect(c.HANGUP_PIN, GPIO.BOTH, callback=HANGUP_BTN_EVENT, bouncetime=90)
#GPIO.add_event_detect(c.HANGUP_PIN, GPIO.RISING, callback=HANGUP_BTN_DOWN, bouncetime=90)

try:
	while True:
		hangupState = GPIO.input(c.HANGUP_PIN)
		button_state_green = GPIO.input(c.GREEN_PIN)
		if button_state_green == GPIO.LOW:
			print("Green button press")
		time.sleep(0.2)
except:
	GPIO.cleanup()

