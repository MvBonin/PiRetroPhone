##Author: Markwart v. Bonin

import RPi.GPIO as GPIO
import datetime
import sys
import dbus
import dbus.mainloop.glib
import wave
import alsaaudio
import yaml

import time

##config.py
import config

##We will use ofono to place calls, hang up etc

class Phone(object):
	"""
	The Phone Class
	"""
	def __init__(self, dial_pin, hangupBtn_pin):
		GPIO.setmode(GPIO.BCM)
		self.dial_pin = dial_pin;
		self.hangupBtn_pin = hangupBtn_pin;


if __name__ == '__main__':

	p = Phone(DIAL_PIN, HANGUP_PIN)

