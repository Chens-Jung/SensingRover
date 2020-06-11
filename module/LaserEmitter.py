import RPi.GPIO as GPIO
import time

class LaserEmitter:
    def __init__(self, laserpin):
        self.__laserpin = laserpin
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(laserpin, GPIO.OUT, initial=GPIO.HIGH)

    def on(self):
        GPIO.output(self.__laserpin, GPIO.LOW)

    def off(self):
        GPIO.output(self.__laserpin, GPIO.HIGH)

    def destroy(self):
        GPIO.output(self.__laserpin, GPIO.HIGH)
        GPIO.cleanup(self.__laserpin)