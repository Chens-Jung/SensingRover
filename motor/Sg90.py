import time
from motor.Pca9685 import Pca9685

class Sg90:
    def __init__(self, pca9685, frequency=50):
        self.__pca9685 = pca9685

        # Pca9685의 출력 주파수(hz)를 설정
        # 대부분의 모터는 50hz를 사용
        pca9685.frequency = frequency

    def __map(self, angle):
        # maxstep(180도) : 553 / minstep(0도) : 164
        return int(164 + angle * ((553-164) / 180))

    def angle(self, channel, angle):
        print("sg90.angle 실행")
        self.__pca9685.write(channel, self.__map(angle))


if __name__ == '__main__':
    pca9685 = Pca9685()
    sg90 = Sg90(pca9685)

    channel = 1

    while True:
        # 0도
        sg90.angle(channel, 0)
        time.sleep(1)

        # 90도
        sg90.angle(channel, 90)
        time.sleep(1)

        # 180도
        sg90.angle(channel, 180)
        time.sleep(1)

    print("Program exit")