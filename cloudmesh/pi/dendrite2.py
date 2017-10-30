import time
import sys
import grovepi
from thread import start_new_thread

states = {"FREE" :0, "RECOVERING" :1, "WORKING":2}

class Dendrite:
	def __init__(self, pin = 3, recovery_time = 20):
		"""
		initialise dendrite with pin and recovery time
		pin = 3 by default, connect relay to port D3 of grovepi
		connect the dendrite to the battery via the relay
		recovery_time = 20 seconds by default
		time taken by dendrite to regain its shape  after current is turned off
		"""

		self.dendrite = pin
		self.recovery_time = recovery_time
		grovepi.pinMode(self.dendrite,"OUTPUT")
		self.setState(states["FREE"])
		print "INIT"

	def recover(self):
		"""
		once the current is turned off, do not turn on until after recovery_time
		"""
		print "recovering"
		time.sleep(self.recovery_time)
		print "recovered"
		self.setState(states["FREE"])

	def on(self):
		"""
		turn on the relay to allow current to flow through the dendrite
		if the dendrite is already in ON state, no point in trying to turn on again
		if the dendrite is recovering, do not try to turn on the relay
		"""
		print "ON called at state", self.state
		if self.state == states["FREE"]:
			self.setState(states["WORKING"])
			grovepi.digitalWrite(self.dendrite,1)
		else:
			print "BUSY"

	def off(self):
		"""
		turn the relay off to allow dendrite to recover to original configuration
		if the denrite has already recovered or is recovering, do not turn off
		"""

		print "OFF called at state", self.state

		grovepi.digitalWrite(self.dendrite,0)
		if self.state == states["WORKING"]:
			self.setState(states["RECOVERING"])
			start_new_thread(self.recover,())
		else:
			print "RELAXING"

	def setState(self,state):
		"""
		set the state of the dendrite
		state = 0 means FREE i.e. the dendrite is not ON and is not recovering and relay can be switched on
		state = 1 means WORKING i.e. the relay is  ON and dendrite is getting heated
		state = 2 means RECOVERING i.e. the relay is OFF and dendrite is trying to recover to its original shape

		to set these states a global states dictionary is used here
		"""

		self.state = state
		print "state =" ,state


if __name__ == "__main__":
	if len(sys.argv) < 2:
		print "Error"
		print "usage: dendrite_test.py <heating time in seconds>"
		print "using heat time of 0.5 seconds"
		heat_time = 0.5
	else:
		heat_time = float(sys.argv[1])

	dendrite0 = Dendrite(pin=2, recovery_time = 10)
	dendrite1 = Dendrite(pin=4, recovery_time = 10)
	dendrite2 = Dendrite(pin=6, recovery_time = 10)
	dendrite3 = Dendrite(pin=8, recovery_time = 10)

	dendrites = [dendrite0, dendrite1, dendrite2, dendrite3]

	msg = "ON ON ON ON"
	m_list = msg.split(" ")
	for i in range(len(dendrites)):
		if  m_list[i] == "ON":
			dendrites[i].on()
		else:
			dendrites[i].off()

	time.sleep(heat_time)
	for dendrite in dendrites:
		dendrite.off()

