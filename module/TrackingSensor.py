import RPi.GPIO as GPIO
import time

class TrackingSensor:
    def __init__(self, trackpin=None):
        self.__trackpin = trackpin
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(trackpin, GPIO.IN)

    def read(self):
        if GPIO.input(self.__trackpin) == GPIO.LOW:
            return 1

        else:
            return 0

    def destroy(self):
        GPIO.cleanup(self.__trackpin)