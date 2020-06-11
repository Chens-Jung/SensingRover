import sys
import os
import time

filepath=os.path.dirname(os.path.dirname(__file__))
sys.path.append(filepath)

from module.Photoresistor import Photoresistor
from module.Thermistor import Thermistor
from module.Gas import Gas

from module.HcSr04 import HcSr04
from module.RgbLed import RgbLed
from module.ActiveBuzzer import ActiveBuzzer
from module.LaserEmitter import LaserEmitter
from module.TrackingSensor import TrackingSensor

from motor.Sg90 import Sg90
from motor.Pca9685 import Pca9685
from module.Lcd1602 import Lcd1602

from module.Pcf8591 import Pcf8591


pcf8591 = Pcf8591(0x48)

photoresistor = Photoresistor(pcf8591, ain=0)
thermistor = Thermistor(pcf8591, ain=1)
gas = Gas(pcf8591, ain=2)
trackingSensor = TrackingSensor(32)
activeBuzzer = ActiveBuzzer(35)
laserEmitter = LaserEmitter(37)
# red = 16, green = 18, blue= 22
rgbLed = RgbLed(redpin=16, greenpin=18, bluepin=22)
pca9685 = Pca9685()
sg90 = Sg90(pca9685)
lcd = Lcd1602(0x27)

ultrasonic = HcSr04(38, 40)

# sg90 = 0
camera_x=1
camera_y=0

ultra_servo = 4
handle_servo = 5


while True:
    # print(thermistor.read())
    # print("{}, {}".format(photoresistor.read(), gas.read()))
    # print(ultrasonic.distance())

    # activeBuzzer.on()
    # time.sleep(2)
    # activeBuzzer.off()
    # break
    # rgbLed.red()
    # time.sleep(0.5)
    # rgbLed.blue()
    # time.sleep(0.5)
    # rgbLed.green()

    # laserEmitter.on()
    # time.sleep(2)
    # laserEmitter.off()
    # break

    print(trackingSensor.read())
    # break


# channel = handle_servo
# while True:
#     sg90.angle(channel, 30)
#     time.sleep(1)
#     sg90.angle(channel, 90)
#     time.sleep(1)
#     sg90.angle(channel, 180)
#     time.sleep(1)
#     sg90.angle(channel, 90)
#     time.sleep(1)

# lcd.write(0, 0, 'Jang Chen')
# lcd.write(0, 1, 'yop yop#%^&@#%*$')
