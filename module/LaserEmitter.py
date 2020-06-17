import RPi.GPIO as GPIO
import time

class LaserEmitter:
    def __init__(self, laserpin):
        self.__laserpin = laserpin
        self.state = "OFF"
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(laserpin, GPIO.OUT, initial=GPIO.HIGH)

    def on(self):
        self.state = "ON"
        GPIO.output(self.__laserpin, GPIO.LOW)

    def off(self):
        self.state = "OFF"
        GPIO.output(self.__laserpin, GPIO.HIGH)

    def destroy(self):
        self.state = "OFF"
        GPIO.output(self.__laserpin, GPIO.HIGH)
        GPIO.cleanup(self.__laserpin)

if __name__ == '__main__':
    laser = LaserEmitter(37)
    laser.on()
    time.sleep(3)

    laser.off()
    time.sleep(3)