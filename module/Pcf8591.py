import smbus


class Pcf8591:
    def __init__(self, addr):
        # Jetson nano 보드에 i2c bus 0, 1 두가지가 있는데, 0은 보드 내부에서 사용하고(우린 사용불가), 1은 우리가 프로그램으로 이용할 수 있다.
        # Jetson nano Board의 I2C Bus 번호 설정
        self.__bus = smbus.SMBus(1)

        # PCF8591의 I2C 장치 번호(주소)
        self.__addr = addr
        
    # AINx로 읽는 메소드, 몇번으로 받을지 정해야 하기 때문에 chn 매개변수 필요
    # channel : AIN0 ~ AIN3
    def read(self, channel):
        try:
            # AIN0 : 0x40
            if channel == 0:
                # PCF8591에게 0x40번에 들어오는 값을 읽겠다고 보드에서 명령을 보내는것
                self.__bus.write_byte(self.__addr, 0x40)
            # AIN1 : 0x41
            elif channel == 1:
                self.__bus.write_byte(self.__addr, 0x41)
            # AIN2 : 0x42
            elif channel == 2:
                self.__bus.write_byte(self.__addr, 0x42)
            # AIN3 : 0x43
            elif channel == 3:
                self.__bus.write_byte(self.__addr, 0x43)

            # 값을 읽기 시작하겠다는 신호(?)
            self.__bus.read_byte(self.__addr)
            value = self.__bus.read_byte(self.__addr)
        except Exception as e:
            print(e)
            value = -1
        return value
    
    # AOUT으로 출력하는 메소드, 어떤값을 보낼지 매개변수 필요
    # value : AOUT으로 출력되는 값
    def write(self, value):
        try:
            # value는 정수여야함
            value = int(value)
            # 0x40 자리에 뭐가 오든, AOUT으로 값을 보낸다.
            # write_byte : 명령을 보내는 것, write_byte_date : 데이터를 보내는 것
            self.__bus.write_byte_data(self.__addr, 0x40, value)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    pcf8591 = Pcf8591(0x48)
    while True:
        value = pcf8591.read(0)
        light = value * (255 - 125) / 255 + 125
        pcf8591.write(light)
