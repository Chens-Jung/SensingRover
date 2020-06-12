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
            print('White line is detected')
            return 1

        else:
            print('Black line is detected')
            return 0

    def destroy(self):
        GPIO.cleanup(self.__trackpin)