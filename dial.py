import config as c
import RPi.GPIO as GPIO
import time
import threading

class Dial:
	def __init__(self):
		self.pulse = 0
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(c.DIAL_PULSE_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		GPIO.setup(c.DIAL_CONTROL_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

		GPIO.add_event_detect(c.DIAL_CONTROL_PIN, GPIO.BOTH)
		self.lastState = GPIO.input(c.DIAL_CONTROL_PIN)
		self.waitingSingleNumber = False


		self.number = ""
		self.listenState = False
		self.timeout = c.DIAL_TIMEOUT
		
		#Wait for numbers
		self.running = False
		
		self.startTime = time.time()
	def counter(self, pin):
		self.pulse = self.pulse + 1
	
	def addToNumber(self,i):
		self.number += str(i)

	def listen(self):
		#start listening
		print("--Dial Listen Start")
		if self.listenState == False:
			self.listenState = True
			self.number = ""

	def stopListen(self):
		print("--Dial Listen Stop")
		if self.listenState == True:
			self.listenState = False
			return self.number

	def isListening(self):
		return self.listenState

	def getSingleNumber(self):
		self.waitingSingleNumber = True
		num = None
		startTime = time.time()
		self.lastState = GPIO.input(c.DIAL_CONTROL_PIN)
		self.curState = GPIO.input(c.DIAL_CONTROL_PIN)
		#print("Waiting for single Number")
		
		while self.waitingSingleNumber:
			if time.time() - startTime > self.timeout:
				return 11
			try:
				if GPIO.event_detected(c.DIAL_CONTROL_PIN):
					self.curState = GPIO.input(c.DIAL_CONTROL_PIN)
				if self.curState != self.lastState:
					if self.curState == False:
						GPIO.add_event_detect(c.DIAL_PULSE_PIN, GPIO.BOTH, callback=self.counter, bouncetime=10)
					else:
						GPIO.remove_event_detect(c.DIAL_PULSE_PIN)
						#print("Pulse detected: ", self.pulse)
						num = int(self.pulse/2)
						#print("Number dialed: ", number)
						self.pulse = 0
						self.waitingSingleNumber = False
					self.lastState = GPIO.input(c.DIAL_CONTROL_PIN)
				
			except KeyboardInterrupt:
				self.waitingSingleNumber = False
			except:
				self.waitingSingleNumber = False
		return num

	def waitForNumbers(self):
		print("Waiting for Numbers")
		#self.startTime = time.time()
		self.running = True
		while self.running:
			##Wait for numbers, Out them after timeout
			self.lastState = GPIO.input(c.DIAL_CONTROL_PIN)
			singleNum = self.getSingleNumber()
			if singleNum != None  and self.isListening():
				if singleNum == 10:
					singleNum = 0
				if singleNum == 11:
					### 11: timeout!
					#self.running = False
					self.listenState = False
				else:
					print("Put Number %s in queue" % singleNum)
					self.addToNumber(singleNum)
		
				

	def start(self):
		##Start Thread that waits for the number
		if self.running == False:
			print("Setting up Dial Thread")
			self.t = threading.Thread(target = self.waitForNumbers)
			self.t.start()

	def stop(self):
		self.running = False