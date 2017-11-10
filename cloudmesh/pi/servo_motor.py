import grovepi
import time 

class Servo:
	def __init__(self, pin = 3, dc = 0):
		"""
		initialise the servo to neutral position dc = 7.5
		"""
		self.servo = pin
		grovepi.pinMode(self.servo, "OUTPUT")
		grovepi.analogWrite(self.servo, dc)

	def setZero(self):
		"""
		set the motor in zero degree position
		"""
		grovepi.analogWrite(self.servo, 0)

	def setNeutral(self):
		"""
		set the motor in neutral position
		"""
		dc = 192
		grovepi.analogWrite(self.servo, dc)

	def setFull(self):
		"""
		set the motor in 90 degrees position
		"""
		dc = 222
		grovepi.analogWrite(self.servo, dc)



if __name__ == "__main__":
	serv = Servo(pin = 3)
	print "Zero"
	serv.setZero()
	time.sleep(1)

	print "Full"
	serv.setFull()
	time.sleep(1)

	print "Neutral"
	serv.setNeutral()

