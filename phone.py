import config as c
import time
import sys
import dbus
import dbus.mainloop.glib
from gi.repository import GLib
from threading import Thread
from threading import Event



class Phone(object):
	
	
	def getManager(self):
		self.manager = dbus.Interface(self.bus.get_object('org.ofono', '/'), 'org.ofono.Manager')
	def getVCM(self):
		return dbus.Interface(self.bus.get_object('org.ofono', self.modem), 'org.ofono.VoiceCallManager')
	def getOnlineModem(self, manager):
		##self.modems = manager.getModems()
		self.manager = dbus.Interface(self.bus.get_object('org.ofono', '/'), 'org.ofono.Manager')
		self.modems = self.manager.GetModems()
		for path, properties in self.modems:
			##properties = modem.GetProperties()
			print("Waiting for online bt device")
			if 'Online' in properties:
				#print("Online modem: %s" % properties['Online'])
				if properties['Online'] == 1:
					return path
	def waitForOnlineModem(self, manager):
		print("Waiting for online Modem")
		found = False
		while found == False:
			modem = self.getOnlineModem( manager )
			if modem != None:
				found = True
				return modem
			time.sleep(0.5)

	def getIncomingCall(self):
		calls = self.vcm.GetCalls()
		for path, properties in calls:
			if properties['State'] == "incoming":
				return path
		pass

	def answerCall(self, path):
		call = dbus.Interface(self.bus.get_object('org.ofono', path), 'org.ofono.VoiceCall')
		call.Answer()

	def __init__(self):
		dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
		print("Phone set up")
		self.bus = dbus.SystemBus()
		self.manager = dbus.Interface(self.bus.get_object('org.ofono', '/'), 'org.ofono.Manager')

		self.modems = self.manager.GetModems()

		self.modem = self.waitForOnlineModem(self.manager)

		print("Modem: %s" % self.modem)
		self.org_ofono_obj = self.bus.get_object('org.ofono', self.modem)
		self.vcm = dbus.Interface(self.org_ofono_obj, 'org.ofono.VoiceCallManager')

		self.call_in_progress = False
		self._setup_dbus_loop()
		print("Initialized Dbus")


	def _setup_dbus_loop(self):
		dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
		self.loop = GLib.MainLoop()
		self._thread = Thread(target=self.loop.run)
		self._thread.start()
		self.org_ofono_obj.connect_to_signal("CallAdded", self.set_call_in_progress, dbus_interface='org.ofono.VoiceCallManager')
		self.org_ofono_obj.connect_to_signal("CallRemoved", self.set_call_ended, dbus_interface='org.ofono.VoiceCallManager')
		##Incoming calls
		calls = self.vcm.GetCalls()



	def set_call_in_progress(self, object, properties):
		print("Call in progress")
		self.call_in_progress = True

	def set_call_ended(self, object):
		print("Call ended!")
		self.call_in_progress = False
	def hangupCall(self):
		self.vcm.HangupAll()
		
	def callNumber(self, number, hide_callerid='default'):
		print("Calling number %s" % number)
		try:
			self.vcm.Dial(str(number), hide_callerid)
		except dbus.exceptions.DBusException as e:
			name = e.get_dbus_name()
			if name == 'org.freedesktop.DBus.Error.UnknownMethod':
				print("Ofono not running")
				#self.start_file("/home/pi/telefonoa/not_connected.wav")
			elif name == 'org.ofono.Error.InvalidFormat':
				print("Invalid dialed number format!")
				#self.start_file("/home/pi/telefonoa/format_incorrect.wav")
			else:
				print(name)
	def close(self):
		self.loop.quit()
