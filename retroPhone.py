import config as c
import dial
import phone
import time
import RPi.GPIO as GPIO

#########################
##This is the main File##
#########################
GPIO.setmode(GPIO.BCM)


##HANGUP_PIN GREEN_PIN
GPIO.setup(c.HANGUP_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(c.GREEN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)


hangupState = GPIO.input(c.HANGUP_PIN)
greenButtonStart = float(0)
dial = dial.Dial()

phone = phone.Phone()

##We want to do seperate stuff when inside a call



def HANGUP_BTN_EVENT(channel):
	#state = GPIO.input(c.HANGUP_PIN)
	if hangupState == GPIO.LOW:
		print("Aufgelegt")
		##auflegen mit Ofono
		if True:
			phone.hangupCall()
	else:
		print("Abgehoben")
		


GPIO.add_event_detect(c.HANGUP_PIN, GPIO.BOTH, callback=HANGUP_BTN_EVENT, bouncetime=90)


def greenBtnPushed(sec):
	print("Green Btn pushed for ", sec, " Seconds.")

def greenBtnFiveSec():
	print("5 Sec um")
	phone.call("017693204140")

### Main Loop
try:
	while True:
		hangupState = GPIO.input(c.HANGUP_PIN)
		button_state_green = GPIO.input(c.GREEN_PIN)

		if button_state_green == GPIO.LOW:
			nowTime = time.time()
			if greenButtonStart == float(0):
				greenButtonStart = time.time()
			elif (nowTime - greenButtonStart) >= float(5):
				greenBtnFiveSec()
		else:
			if greenButtonStart != float(0):
				nowTime =time.time()
				#print("Time elapsed for green Button: ", nowTime - greenButtonStart)
				greenBtnPushed((nowTime - greenButtonStart))
				greenButtonStart = float(0)

		if hangupState == GPIO.LOW:
			##Is Picked up
			print("Pick Up")
		time.sleep(0.2)
except:
	GPIO.cleanup()
