import config as c
import RPi.GPIO as GPIO
import time


class Dial:
	def __init__(self):
		self.pulse = 0
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(c.DIAL_PULSE_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		GPIO.setup(c.DIAL_CONTROL_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

		GPIO.add_event_detect(c.DIAL_CONTROL_PIN, GPIO.BOTH)
		lastState = GPIO.input(c.DIAL_CONTROL_PIN)
		self.waiting = False
	def counter(pin):
		self.pulse = self.pulse + 1
	
	def getNumber(self):
		self.waiting = True
		while self.waiting:
			try:
				if GPIO.event_detected(c.DIAL_CONTROL_PIN):
					curState = GPIO.input(c.DIAL_CONTROL_PIN)
				if curState != lastState:
					if curState == False:
						GPIO.add_event_detect(c.DIAL_PULSE_PIN, GPIO.BOTH, callback=counter, bouncetime=10)
					else:
						GPIO.remove_event_detect(c.DIAL_PULSE_PIN)
						#print("Pulse detected: ", pulse)
						number = int(pulse/2)
						print("Number dialed: ", number)
						pulse = 0
						self.waiting = False
					lastState = GPIO.input(c.DIAL_CONTROL_PIN)
			except KeyboardInterrupt:
				GPIO.cleanup()
			except:
				GPIO.cleanup()