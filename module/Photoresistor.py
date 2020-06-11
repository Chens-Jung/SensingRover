import time
from module.Pcf8591 import Pcf8591

class Photoresistor:
    def __init__(self, pcf8591, ain=0):
        self.__pcf8591 = pcf8591
        self.__ain = ain

    def read(self):
        photo = self.__pcf8591.read(self.__ain)
        return photo

if __name__ == '__main__':
    pcf8591 = Pcf8591(0x48)
    photo_sensor = Photoresistor(pcf8591, ain=0)

    try:
        while True:
            value = photo_sensor.read()
            print(value)
            time.sleep(1)
    except KeyboardInterrupt:
        print()
    finally:
        print("Program exit")