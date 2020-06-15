import RPi.GPIO as GPIO
import time
import threading

class HcSr04(threading.Thread):
    def __init__(self, trigpin=None, echopin=None):
        self.__trigpin = trigpin
        self.__echopin = echopin
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(trigpin, GPIO.OUT)
        GPIO.setup(echopin, GPIO.IN)
        self.value = 0
        super().__init__(target=self.distance)
        super().start()

    def distance(self):
        while True:
            # trigger pin High, 10마이크로초 동안 유지
            GPIO.output(self.__trigpin, GPIO.HIGH)
            time.sleep(0.00001)

            # trigger pin Low(초음파 발생)
            GPIO.output(self.__trigpin, GPIO.LOW)

            startTime = time.time()
            stopTime = time.time()

            cnt = 0
            # echopin이 High 상태로 변할때까지 기다림
            while GPIO.input(self.__echopin) == GPIO.LOW:
                cnt += 1
                startTime = time.time()
                if cnt > 100000:
                    return self.distance()

            cnt = 0
            # echopin이 Low 상태로 변할때까지 기다림
            while GPIO.input(self.__echopin) == GPIO.HIGH:
                cnt += 1
                stopTime = time.time()
                if cnt > 100000:
                    return self.distance()


            # 거리 계산(단위: cm)
            during = stopTime - startTime
            dist = during * (343 / 2) * 100
            self.value = dist
            time.sleep(1)
            # return dist

#########################################################
if __name__ == "__main__":
    try:
        sensor = HcSr04(trigpin=38, echopin=40)
        while True:
            # distance = sensor.distance()
            print("거리: {}".format(sensor.value))
            time.sleep(0.3)
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()
        print("Program Exit")




