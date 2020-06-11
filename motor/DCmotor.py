import RPi.GPIO as GPIO
from motor.Pca9685 import Pca9685
import time

class DCmotor:
	def __init__(self, out1, out2, pca9685, pwm):
		self.__out1 = out1
		self.__out2 = out2
		GPIO.setmode(GPIO.BOARD)
		GPIO.setwarnings(False)
		GPIO.setup(out1, GPIO.OUT, initial=GPIO.LOW)
		GPIO.setup(out2, GPIO.OUT, initial=GPIO.LOW)
		self.__pca9685 = pca9685
		self.__pwm = pwm

	def setSpeed(self, step):
		self.__pca9685.write(self.__pwm, step)

	def forward(self):
		GPIO.output(self.__out1, GPIO.HIGH)
		GPIO.output(self.__out2, GPIO.LOW)

	def backward(self):
		GPIO.output(self.__out1, GPIO.LOW)
		GPIO.output(self.__out2, GPIO.HIGH)

	def stop(self):
		GPIO.output(self.__out1, GPIO.HIGH)
		GPIO.output(self.__out2, GPIO.HIGH)
		self.setSpeed(0)

if __name__ =="__main__":
	pca9685 = Pca9685()

	dcMotor1 = DCmotor(11,12,pca9685, 5)
	dcMotor2 = DCmotor(13,15,pca9685, 4)

	dcMotor1.forward()
	dcMotor2.forward()

	dcMotor1.setSpeed(4000)
	dcMotor2.setSpeed(4000)

	time.sleep(3)

	dcMotor1.stop()
	dcMotor2.stop()
	time.sleep(2)

	# dcMotor1.backward()
	# dcMotor2.backward()
	# dcMotor1.setSpeed(4095)
	# dcMotor2.setSpeed(4095)
	# time.sleep(5)
	#
	# dcMotor1.stop()
	# dcMotor2.stop()
	# time.sleep(2)
