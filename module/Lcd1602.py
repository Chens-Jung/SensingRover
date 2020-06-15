import time
import smbus
import socket
from module.Pcf8591 import Pcf8591
from module.Thermistor import Thermistor

class Lcd1602:
	def __init__(self, addr):
		self.__bus = smbus.SMBus(1)
		self.__addr = addr
		self.state1 = ""
		self.state2 = ""
		self.init()


	def init(self):
		try:
			self.send_command(0x33) # Must initialize to 8-line mode at first
			time.sleep(0.005)
			self.send_command(0x32) # Then initialize to 4-line mode
			time.sleep(0.005)
			self.send_command(0x28) # 2 Lines & 5*7 dots
			time.sleep(0.005)
			self.send_command(0x0C) # Enable display without cursor
			time.sleep(0.005)
			self.send_command(0x01) # Clear Screen
			self.__bus.write_byte(self.__addr, 0x08)
		except:
			return False
		else:
			return True

	def write_word(self, data):
		temp = data | 0x08
		self.__bus.write_byte(self.__addr ,temp)

	def send_command(self, comm):
		# Send bit7-4 firstly
		buf = comm & 0xF0
		buf |= 0x04               # RS = 0, RW = 0, EN = 1
		self.write_word(buf)
		time.sleep(0.002)
		buf &= 0xFB               # Make EN = 0
		self.write_word(buf)

		# Send bit3-0 secondly
		buf = (comm & 0x0F) << 4
		buf |= 0x04               # RS = 0, RW = 0, EN = 1
		self.write_word(buf)
		time.sleep(0.002)
		buf &= 0xFB               # Make EN = 0
		self.write_word(buf)

	def send_data(self, data):
		# Send bit7-4 firstly
		buf = data & 0xF0
		buf |= 0x05               # RS = 1, RW = 0, EN = 1
		self.write_word(buf)
		time.sleep(0.002)
		buf &= 0xFB               # Make EN = 0
		self.write_word(buf)

		# Send bit3-0 secondly
		buf = (data & 0x0F) << 4
		buf |= 0x05               # RS = 1, RW = 0, EN = 1
		self.write_word(buf)
		time.sleep(0.002)
		buf &= 0xFB               # Make EN = 0
		self.write_word(buf)

	def clear(self):
		self.send_command(0x01) # Clear Screen

	def openlight(self):  # Enable the backlight
		self.__bus.write_byte(0x27,0x08)
		self.__bus.close()

	def write(self, x, y, str):
		# y : 세로축(행), x : 가로축(열)
		if x < 0:
			x = 0
		if x > 15:
			x = 15
		if y <0:
			y = 0
		if y > 1:
			y = 1

		if y == 0:
			self.state1 = str
		else:
			self.state2 = str

		# Move cursor
		addr = 0x80 + 0x40 * y + x
		self.send_command(addr)

		for chr in str:
			self.send_data(ord(chr))

def get_local_ip1():
	print(socket.gethostbyname('COM-PC'))
	print(socket.gethostbyname_ex("COM-PC"))


def get_local_ip2(network_address):
	ip_list = socket.gethostbyname_ex(socket.gethostname())[2]
	for ip in ip_list:
		if network_address in ip:
			return ip
	return None

def get_local_ip3():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(('192.168.3.1', 0))
	ipAddress = s.getsockname()[0]
	s.close()
	return ipAddress



if __name__ == '__main__':
	lcd = Lcd1602(0x27)
	lcd.write(0, 0, 'Hello')
	lcd.write(0, 1, 'AIOT class!')

