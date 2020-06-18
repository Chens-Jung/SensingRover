import RPi.GPIO as GPIO
import time

class ActiveBuzzer:
    ON = "on"
    OFF = "off"

    def __init__(self, channel):
        self.__channel = channel
        self.state = ActiveBuzzer.OFF
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(channel, GPIO.OUT, initial=GPIO.HIGH)

    def on(self):
        self.state = ActiveBuzzer.ON
        GPIO.output(self.__channel, GPIO.LOW)

    def off(self):
        self.state = ActiveBuzzer.OFF
        GPIO.output(self.__channel, GPIO.HIGH)

    def active(self):
        for i in range(4):
            GPIO.output(self.__channel, GPIO.LOW)
            self.state = ActiveBuzzer.ON
            time.sleep(0.3)
            self.state = ActiveBuzzer.OFF
            GPIO.output(self.__channel, GPIO.HIGH)
            time.sleep(0.3)


if __name__ == '__main__':
    try:
        buzzer = ActiveBuzzer(35)
        # for i in range(5):
        #     buzzer.on()
        #     time.sleep(0.5)
        #     buzzer.off()
        #     time.sleep(0.5)
        buzzer.active()

    except KeyboardInterrupt:
        print()
    finally:
        buzzer.off()
        print("program exit")