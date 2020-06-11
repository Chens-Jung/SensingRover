import RPi.GPIO as GPIO
import time

class TrackingSensor:
    def __init__(self, trackpin=None):
        self.__trackpin = trackpin
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(trackpin, GPIO.IN)

    def read(self):
        while True:
            if GPIO.input(self.__trackpin) == GPIO.LOW:
                print('White line is detected')

            else:
                print('Black line is detected')

            time.sleep(1)

    def destroy(self):
        GPIO.cleanup(self.__trackpin)