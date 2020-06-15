import RPi.GPIO as GPIO
import threading
import time

class TrackingSensor(threading.Thread):
    WHITE_LINE = 0
    BLACK_LINE = 1

    def __init__(self, trackpin=None):
        self.__trackpin = trackpin
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(trackpin, GPIO.IN)
        self.value = 0
        super().__init__(target=self.read)
        super().start()

    def read(self):
        while True:
            if GPIO.input(self.__trackpin) == GPIO.LOW:
                self.value = TrackingSensor.WHITE_LINE

            else:
                self.value = TrackingSensor.BLACK_LINE
            time.sleep(1)

    def destroy(self):
        GPIO.cleanup(self.__trackpin)