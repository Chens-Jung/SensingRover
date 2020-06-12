import time
from module.Pcf8591 import Pcf8591

class Gas():
    def __init__(self, pcf8591, ain=0):
        self.__pcf8591 = pcf8591
        self.__ain = ain

    def read(self):
        value = self.__pcf8591.read(self.__ain)
        return value

if __name__ == '__main__':
    pcf8591 = Pcf8591(0x48)
    gas = Gas(pcf8591, ain=0)

    try:
        while True:
            value = gas.read()
            print(value)
            time.sleep(1)
    except KeyboardInterrupt:
        print()
    finally:
        print("program exit")