import config as c
import RPi.GPIO as GPIO
import time
import threading

class Ringer(object):
	def __init__(self):
		###Set up the Ringer GPIO
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(c.RING_PIN, GPIO.OUT)

		self.state = False
		self.pauseTime = 1.0
		self.sleepLow = 0.02
		self.sleepHigh = 0.008
		self.singleRingCount = 50

	def close(self):
		GPIO.cleanup()

	def fillRingList(self):
		self.RingStyles = list("-.-.")
		self.RingStyles.extend("--.")
		self.RingStyles.extend("--.-.-")

	def getRingListSize(self):
		return len(self.RingStyles)
	def getRingStyle(index):
		if len(self.RingStyles) < index:
			return self.RingStyles[index]

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
			GPIO.output(c.RING_PIN, GPIO.HIGH)
			i = i + 1
		##put it high now
		GPIO.output(c.RING_PIN, GPIO.HIGH)

	def ring(self, ringStyle):
		if ringStyle != "":
			print("Ring it")
			self.state = True
			try:
				while self.state:
					for letter in ringStyle:
						if isCharacterRing(letter):
							singleRing(self.singleRingCount)
						else:
							sleep(self.pauseTime)
				print("Stopped Ring")
			except:
				self.close()

	def stop(self):
		self.state = False

