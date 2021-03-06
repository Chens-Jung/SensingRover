import sys
import os
import json
import time

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
        # 3.28 씽씽카 번호
        self.__camera_y_servo = 0
        self.__camera_x_servo = 1
        self.__ultrasonic_servo = 2
        self.__handle_servo = 3
        # 3.23 씽씽카 번호
        # self.__ultrasonic_servo = 7
        # self.__camera_y_servo = 11
        # self.__camera_x_servo = 9
        # self.__handle_servo = 15

        # 기본 상태 설정
        self.__dcMotor_state = "stop"
        self.__handle_angle = 90
        self.__dcMotor_speed = 0
        self.__camera_x_angle = 90
        self.__camera_y_angle = 90
        self.__distance_angle = 90


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
        self.__message["dcMotor_speed"] = self.__dcMotor_speed
        jsonMessage = json.dumps(self.__message)
        return jsonMessage

    def lcd_test(self, message):
        self.__lcd.clear()
        self.__lcd.write(0, 0, message["lcd0"])
        self.__lcd.write(0, 1, message["lcd1"])

    # ------------------------------------------------------

    # motor -------------------------------------------------
    def angle_camera_left(self):
        if self.__camera_x_angle >= 2:
            self.__camera_x_angle -= 2
            self.__sg90.angle(self.__camera_x_servo, self.__camera_x_angle)

    def angle_camera_right(self):
        if self.__camera_x_angle <= 178:
            self.__camera_x_angle += 2
            self.__sg90.angle(self.__camera_x_servo, self.__camera_x_angle)

    def angle_camera_front(self):
        if self.__camera_y_angle >= 2:
            self.__camera_y_angle -= 2
        self.__sg90.angle(self.__camera_y_servo, self.__camera_y_angle)

    def angle_camera_back(self):
        if self.__camera_y_angle <= 178:
            self.__camera_y_angle += 2
        self.__sg90.angle(self.__camera_y_servo, self.__camera_y_angle)

    # def angle_ultrasonic(self, angle):
    #     self.__sg90.angle(self.__ultrasonic_servo, angle)

    def angle_distance_left(self):
        if self.__distance_angle >= 2:
            self.__distance_angle -= 2
            self.__sg90.angle(self.__ultrasonic_servo, self.__distance_angle)

    def angle_distance_right(self):
        if self.__distance_angle <= 178:
            self.__distance_angle += 2
            self.__sg90.angle(self.__ultrasonic_servo, self.__distance_angle)

    def handle_left(self):
        if self.__handle_angle >= 2:
            self.__handle_angle -= 2
            self.__sg90.angle(self.__handle_servo, self.__handle_angle)
    def handle_right(self):
        if self.__handle_angle <= 178:
            self.__handle_angle += 2
            self.__sg90.angle(self.__handle_servo, self.__handle_angle)

    def handle_refront(self):
        while True:
            if self.__handle_angle == 90:
                break
            if self.__handle_angle == 91:
                break
            if self.__handle_angle == 89:
                break

            if self.__handle_angle < 90:
                self.__handle_angle += 1
            else:
                self.__handle_angle -= 1
            self.__sg90.angle(self.__handle_servo, self.__handle_angle)

    def forward(self):
        self.__dcMotor_state = "forward"
        if self.__dcMotor_speed < 4050:
            self.__dcMotor_speed += 50
        self.setSpeed(self.__dcMotor_speed)
        print(self.__dcMotor_speed)
        self.__dcMotor1.forward()
        self.__dcMotor2.forward()

    def backward(self):
        self.__dcMotor_state = "backward"
        if self.__dcMotor_speed < 4050:
            self.__dcMotor_speed += 50
        self.setSpeed(self.__dcMotor_speed)
        print(self.__dcMotor_speed)
        self.__dcMotor1.backward()
        self.__dcMotor2.backward()

    def setSpeed(self, pwm):
        self.__dcMotor1.setSpeed(pwm)
        self.__dcMotor2.setSpeed(pwm)
        self.__dcMotor_speed = pwm

    def stop(self):
        self.__dcMotor_state = "stop"
        self.__dcMotor_speed = 0
        self.__dcMotor1.stop()
        self.__dcMotor2.stop()

    def respeed(self):
        self.__dcMotor_speed = 0
        self.setSpeed(self.__dcMotor_speed)
        print(self.__dcMotor_speed)

    def button_forward(self):
        self.__dcMotor_state = "forward"
        self.__dcMotor1.forward()
        self.__dcMotor2.forward()

    def button_backward(self):
        self.__dcMotor_state = "backward"
        self.__dcMotor1.backward()
        self.__dcMotor2.backward()

    def button_stop(self):
        self.__dcMotor_state = "stop"
        self.__dcMotor_speed = 0
        self.__dcMotor1.stop()
        self.__dcMotor2.stop()

    def button_setSpeed(self, pwm):
        print(pwm)
        self.__dcMotor_speed = pwm
        self.__dcMotor1.setSpeed(pwm)
        self.__dcMotor2.setSpeed(pwm)

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