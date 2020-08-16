import config as c
import dial
import phone
import ringer

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








phone = phone.Phone()
ringer = ringer.Ringer()

dial = dial.Dial()
dial.start()

isDialListening = False
incomingCall = None

##Interrupt number event
interruptNumber = False
##Start listening to the dial
def startDialListen():
	global isDialListening
	if not isDialListening:
		print("Let the Dial listen")
		dial.listen()
		isDialListening = True

###EVENT: After Dialing finished
def afterDialListening():
	global isDialListening
	global interruptNumber
	isDialListening = False
	if not interruptNumber:
		print("Dial done, number %s" % dial.number)
	else:
		interruptNumber = False

def HANGUP_BTN_EVENT(channel):
	global incomingCall
	global isDialListening
	global interruptNumber
	#state = GPIO.input(c.HANGUP_PIN)
	if hangupState == GPIO.LOW:
		print("Aufgelegt")
		##auflegen mit Ofono
		if phone.call_in_progress:
			phone.hangupCall()
		
		#evtl stop dial
		##Interrupt number recognition
		interruptNumber = True
		dial.stopListen()
		
		



GPIO.add_event_detect(c.HANGUP_PIN, GPIO.BOTH, callback=HANGUP_BTN_EVENT, bouncetime=90)


def greenBtnPushed(sec):
	print("Green Btn pushed for ", sec, " Seconds.")
	if not dial.isListening() and not isDialListening:
		num = dial.number
		print(num)
	else:
		print("Still listening on dial?")



def greenBtnFiveSec():
	print("5 Sec um, trying to call")
	#phone.callNumber("017693204140")
	ringer.start()

### Main Loop
try:
	while True:
		hangupState = GPIO.input(c.HANGUP_PIN)
		button_state_green = GPIO.input(c.GREEN_PIN)

		if isDialListening == True and not dial.isListening():
			##Listening to the dial has stopped
			afterDialListening()
			
			
		incomingCall = phone.getIncomingCall()

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
			if ringer.state == True:
				ringer.stop()
			if not dial.isListening() and not isDialListening:
				startDialListen()

			if incomingCall != None:
				print("Incoming call is answered")
				phone.answerCall(incomingCall)
				incomingCall = None
		
		
		if incomingCall != None:
			print("Call incoming")
			if ringer.state == False:
				ringer.start()
		time.sleep(0.2)
except:
	phone.close()
	dial.stop()
	ringer.stop()
	GPIO.cleanup()
