import RPi.GPIO as GPIO
import time


class RgbLed:
    RED = "red"
    GREEN = "green"
    BLUE = "blue"

    def __init__(self, redpin=None, greenpin=None, bluepin=None):
        self.__redpin = redpin
        self.__greenpin = greenpin
        self.__bluepin = bluepin
        self.state = None
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        if redpin is not None:
            GPIO.setup(self.__redpin, GPIO.OUT, initial=GPIO.HIGH)
        if greenpin is not None:
            GPIO.setup(self.__greenpin, GPIO.OUT, initial=GPIO.HIGH)
        if bluepin is not None:
            GPIO.setup(self.__bluepin, GPIO.OUT, initial=GPIO.HIGH)

    def red(self):
        self.state = RgbLed.RED
        if self.__redpin is not None:
            GPIO.output(self.__redpin, GPIO.LOW)
        # if self.__greenpin is not None:
        #   GPIO.output(self.__greenpin, GPIO.HIGH)
        if self.__bluepin is not None:
            GPIO.output(self.__bluepin, GPIO.HIGH)

    def green(self):
        self.state = RgbLed.GREEN
        # if self.__redpin is not None:
        #   GPIO.output(self.__redpin, GPIO.HIGH)
        if self.__greenpin is not None:
            GPIO.output(self.__greenpin, GPIO.LOW)
        if self.__bluepin is not None:
            GPIO.output(self.__bluepin, GPIO.HIGH)

    def blue(self):
        self.state = RgbLed.BLUE
        if self.__redpin is not None:
            GPIO.output(self.__redpin, GPIO.HIGH)
        if self.__greenpin is not None:
            GPIO.output(self.__greenpin, GPIO.HIGH)
        if self.__bluepin is not None:
            GPIO.output(self.__bluepin, GPIO.LOW)

    def off(self):
        self.state = None
        if self.__redpin is not None:
            GPIO.output(self.__redpin, GPIO.HIGH)
        if self.__greenpin is not None:
            GPIO.output(self.__greenpin, GPIO.HIGH)
        if self.__bluepin is not None:
            GPIO.output(self.__bluepin, GPIO.HIGH)


if __name__ == "__main__":
    try:
        rgbLed = RgbLed(11, 12, 13)
        for i in range(2):
            rgbLed.red()
            time.sleep(1)
            rgbLed.off()

            rgbLed.green()
            time.sleep(1)
            rgbLed.off()

            rgbLed.blue()
            time.sleep(1)
            rgbLed.off()

    # Ctrl+C
    except KeyboardInterrupt:
        print()

    finally:
        rgbLed.off()
        print("program exit")
