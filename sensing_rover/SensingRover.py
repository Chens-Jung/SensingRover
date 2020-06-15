import sys
import os
import threading
import json
import time
import paho.mqtt as mqtt
import RPi.GPIO as GPIO

filepath=os.path.dirname(os.path.dirname(__file__))
sys.path.append(filepath)

from module.ActiveBuzzer import ActiveBuzzer
from module.LaserEmitter import LaserEmitter
from module.RgbLed import RgbLed
from module.Lcd1602 import Lcd1602

from module.Pcf8591 import Pcf8591
from module.Gas import Gas
from module.Photoresistor import Photoresistor
from module.Thermistor import Thermistor
from module.HcSr04 import HcSr04
from module.TrackingSensor import TrackingSensor


class SensingRover:
    def __init__(self):
        # 센서 아닌 모듈
        self.__activeBuzzer = ActiveBuzzer(35)
        self.__laserEmitter = LaserEmitter(37)
        self.__rgbLed = RgbLed(redpin=16, greenpin=18, bluepin=22)
        self.__lcd = Lcd1602(0x27)

        # 센서 모듈
        self.__pcf8591 = Pcf8591(0x48)
        self.__photoresistor = Photoresistor(self.__pcf8591, ain=0)
        self.__thermistor = Thermistor(self.__pcf8591, ain=1)
        self.__gas = Gas(self.__pcf8591, ain=2)
        self.__ultrasonic = HcSr04(trigpin=38, echopin=40)
        self.__tracking = TrackingSensor(32)

        # 메시지
        self.__message = {}

        # 모터

    # module not sensor----------------------------------
    # buzzer method
    def buzzerOn(self):
        self.__activeBuzzer.on()
    def buzzerOff(self):
        self.__activeBuzzer.off()

    # laser method
    def laserOn(self):
        self.__laserEmitter.on()
    def laserOff(self):
        self.__laserEmitter.off()

    # rgbLed method
    def ledRed(self):
        self.__rgbLed.red()
    def ledGreen(self):
        self.__rgbLed.green()
    def ledBlue(self):
        self.__rgbLed.blue()
    def ledOff(self):
        self.__rgbLed.off()

    # lcd method
    def lcdWrite(self, x1, y1, data1, x2, y2, data2):
        self.__lcd.write(x1, y1, data1)
        self.__lcd.write(x2, y2, data2)
    # -----------------------------------------------------

    # sensor moduel----------------------------------------
    # gas method
    def gasRead(self):
        gas_value = self.__gas.read()
        return gas_value

    def sensorRead(self):
        self.__message["gas"] = self.__gas.read()
        self.__message["photoresistor"] = self.__photoresistor.read()
        self.__message["thermistor"] = self.__thermistor.read()
        self.__message["ultrasonic"] = self.__ultrasonic.distance()
        self.__message["tracking"] = self.__tracking.read()



        jsonMessage = json.dumps(self.__message)
        return jsonMessage




