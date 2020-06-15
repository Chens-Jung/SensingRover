import time
from module.Pcf8591 import Pcf8591
import threading

class Photoresistor(threading.Thread):
    def __init__(self, pcf8591, ain=0):
        self.__pcf8591 = pcf8591
        self.__ain = ain
        self.value = 0
        super().__init__(target=self.read)
        self.start()

    def read(self):
        while True:
            photo = self.__pcf8591.read(self.__ain)
            self.value = photo
            time.sleep(1)

if __name__ == '__main__':
    pcf8591 = Pcf8591(0x48)
    photo_sensor = Photoresistor(pcf8591, ain=0)

    try:
        while True:
            value = photo_sensor.value
            print(value)
            time.sleep(0.5)
    except KeyboardInterrupt:
        print()
    finally:
        print("Program exit")