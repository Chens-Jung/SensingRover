import time
import math
from module.ActiveBuzzer import ActiveBuzzer
from module.RgbLed import RgbLed
from module.Pcf8591 import Pcf8591

class Thermistor:
    def __init__(self, pcf8591, ain=0):
        self.__pcf8591 = pcf8591
        self.__ain = ain

    def read(self):
        analog = self.__pcf8591.read(self.__ain)
        temp = 5 * float(analog) / 255
        temp = 10000 * temp / (5 - temp)
        temp = 1 / (((math.log(temp / 10000)) / 3950) + (1 / (273.15 + 25)))

        return temp - 273.15


if __name__ == '__main__':
    try:
        pcf8591 = Pcf8591(0x48)
        sensor = Thermistor(pcf8591, ain=0)
        buzzer = ActiveBuzzer(11)
        led = RgbLed(redpin=13)
        while True:
            temperature = sensor.read()
            print('섭씨 온도: {}도'.format(temperature))
            if temperature > 30:
                led.red()
                buzzer.on()
            else:
                led.off()
                buzzer.off()
            time.sleep(1)
    except KeyboardInterrupt:
        print()
    finally:
        print("Program exit")