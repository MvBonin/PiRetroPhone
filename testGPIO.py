import config as c
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

##HANGUP_PIN GREEN_PIN
#GPIO.setup(c.HANGUP_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP) #GPIO button
#GPIO.setup(c.GREEN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(c.RING_PIN, GPIO.OUT)

try:
	i = 0
	while True:
		i = 0
		while i <= 50:
			#button_state_hangup = GPIO.input(c.HANGUP_PIN)
			#button_state_green = GPIO.input(c.GREEN_PIN)
			#if button_state_hangup == GPIO.LOW:
				#print("Phone is Picked up")
			#if button_state_green == GPIO.LOW:
				#print("Green button press")
			time.sleep(0.02)
			GPIO.output(c.RING_PIN, GPIO.HIGH)
			time.sleep(0.008)
			GPIO.output(c.RING_PIN, GPIO.LOW)
			i = i + 1
		GPIO.output(c.RING_PIN, GPIO.HIGH)
		time.sleep(1)
except:
	GPIO.cleanup()
