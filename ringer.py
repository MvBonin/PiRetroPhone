import config as c
import RPi.GPIO as GPIO
import time
import threading

class Ringer(object):
	def __init__(self):
		###Set up the Ringer GPIO
		#GPIO.setmode(GPIO.BCM)
		GPIO.setup(c.RING_PIN, GPIO.OUT)
		self.t = None
		self.state = False
		self.pauseTime = 1.0
		self.sleepLow = 0.02
		self.sleepHigh = 0.008
		self.singleRingCount = 30
		self.fillRingList()
		self.currentRingStyle = "-.-."

	def close(self):
		print("Ringer closing itself")
		GPIO.cleanup()

	def fillRingList(self):
		self.RingStyles = list("-.-.")
		self.RingStyles.extend("--.")
		self.RingStyles.extend("--.-.-")

	def getRingListSize(self):
		return len(self.RingStyles)

	def getRingStyle(index):
		return "--.."
		if len(self.RingStyles) > index:
			return self.RingStyles[index]
		else:
			return self.RingStyles[0]

	def isCharacterRing(self, character):
		if character == '-':
			return True
		else:
			return False

	def singleRing(self, timer):
		i = 0
		while i <= int(timer):
			time.sleep(self.sleepLow)
			GPIO.output(c.RING_PIN, GPIO.HIGH)
			time.sleep(self.sleepHigh)
			GPIO.output(c.RING_PIN, GPIO.LOW)
			i = i + 1
		##put it high now
		GPIO.output(c.RING_PIN, GPIO.HIGH)

	def ring(self):

		if self.currentRingStyle != "":
			self.state = True
			try:
				while self.state:
					for letter in self.currentRingStyle:
						if self.isCharacterRing(letter):
							self.singleRing(self.singleRingCount)
						else:
							time.sleep(self.pauseTime)
				print("Stopped Ring")
			except:
				self.close()
	def start(self):
		if self.state == False:
			self.t = threading.Thread(target = self.ring)
			print("Starting Ringing with ringstyle %s" % self.currentRingStyle)
			self.t.start()
	
	def stop(self):
		self.state = False

