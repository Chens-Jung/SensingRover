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

from motor.Pca9685 import Pca9685
from motor.Sg90 import Sg90
from motor.DCmotor import DCmotor


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
        self.__pca9685 = Pca9685()
        self.__sg90 = Sg90(self.__pca9685)
        self.__dcMotor1 = DCmotor(11, 12, self.__pca9685, 5)
        self.__dcMotor2 = DCmotor(13, 15, self.__pca9685, 4)
        self.__camera_y_servo = 0
        self.__camera_x_servo = 1
        self.__ultrasonic_servo = 2
        self.__handle_servo = 3
        self.__dcMotor_state = "stop"


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

    # sensor module----------------------------------------
    def gasRead(self):
        gas_value = self.__gas.read()
        return gas_value

    def sensorRead(self):
        self.__message["gas"] = self.__gas.value
        self.__message["photoresistor"] = self.__photoresistor.value
        self.__message["thermistor"] = self.__thermistor.value
        self.__message["ultrasonic"] = self.__ultrasonic.value
        self.__message["tracking"] = self.__tracking.value

        self.__message["rgbLed_state"] = self.__rgbLed.state
        self.__message["laseremmiter_state"] = self.__laserEmitter.state
        self.__message["buzzer_state"] = self.__activeBuzzer.state
        self.__message["lcd_state"] = "0:"+self.__lcd.state1 + ", 1:" + self.__lcd.state2

        self.__message["dcMotor_state"] = self.__dcMotor_state
        jsonMessage = json.dumps(self.__message)
        return jsonMessage

    def lcd_test(self, message):
        self.__lcd.clear()
        self.__lcd.write(0, 0, message["lcd0"])
        self.__lcd.write(0, 1, message["lcd1"])

    # ------------------------------------------------------

    # motor -------------------------------------------------
    def angle_camera_x(self, angle):
        self.__sg90.angle(self.__camera_x_servo, angle)
    def angle_camera_y(self, angle):
        self.__sg90.angle(self.__camera_y_servo, angle)
    def angle_ultrasonic(self, angle):
        self.__sg90.angle(self.__ultrasonic_servo, angle)
    def angle_handle(self, angle):
        self.__sg90.angle(self.__handle_servo, angle)


    def forward(self):
        self.__dcMotor_state = "forward"
        self.__dcMotor1.forward()
        self.__dcMotor2.forward()

    def backward(self):
        self.__dcMotor_state = "backward"
        self.__dcMotor1.backward()
        self.__dcMotor2.backward()

    def setSpeed(self, pwm):
        self.__dcMotor1.setSpeed(pwm)
        self.__dcMotor2.setSpeed(pwm)

    def stop(self):
        self.__dcMotor_state = "stop"
        self.__dcMotor1.stop()
        self.__dcMotor2.stop()


if __name__ == '__main__':
    sr = SensingRover()
    sr.forward()
    sr.setSpeed(1000)
    time.sleep(2.5)

    sr.stop()

    sr.backward()
    sr.setSpeed(1500)
    time.sleep(2.5)
    sr.stop()