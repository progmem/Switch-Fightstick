from collections import OrderedDict

# serial format
class SendFormat:
	def __init__(self):
		# This format structure needs to be the same as the one written in Joystick.c
		self.format = OrderedDict([
			('cmd', 'p'),
			('btn', '00000000000000'),	# send bit array for buttons
			('lx', 128),
			('ly', 128),
			('rx', 128),
			('ry', 128),
			('hat', 8),
		])

	def setButton(self, btn):
		self.format['btn'] = btn.getBitArray()

	def setDirection(self, dir):
		dir_dic = dir.getDirectDict()
		self.format['lx'] = dir_dic['lx']
		self.format['ly'] = dir_dic['ly']
		self.format['rx'] = dir_dic['rx']
		self.format['ry'] = dir_dic['ry']

	def convert2str(self):
		str_format = ''
		for v in self.format.values():
			str_format += str(v)
			str_format += ' '
		return str_format[:-1] # the last space is not needed


class Buttons:
	def __init__(self, btn_str):
		self.btn_array = btn_str.split()
		self.bit_btn_array = ''

	def getBitArray(self):
		self.bit_btn_array = ''
		self.createBitArray()
		return self.bit_btn_array

	def createBitArray(self):
		# push bits in the order of the format
		self.pushBit('A')
		self.pushBit('B')
		self.pushBit('X')
		self.pushBit('Y')
		self.pushBit('L')
		self.pushBit('R')
		self.pushBit('ZL')
		self.pushBit('ZR')
		self.pushBit('MINUS')
		self.pushBit('PLUS')
		self.pushBit('LCLICK')
		self.pushBit('RCLICK')
		self.pushBit('HOME')
		self.pushBit('CAP')
	
	def pushBit(self, btn):
		if (btn in self.btn_array):
			self.bit_btn_array += '1'
		else:
			self.bit_btn_array += '0'

# as of now, we don't handle HAT button
class Directions:
	def __init__(self, dir_str):
		self.dir_array = dir_str.split()
		self.dir_dic = { 'lx':128, 'ly':128, 'rx':128, 'ry':128 } # 128 means center

	def getDirectDict(self):
		return self.dir_dic

	def createDirectionDict(self):
		pass

# handles serial input to Joystick.c
class KeyPress:
	def __init__(self, ser):
		self.ser = ser
		self.format = SendFormat()
	
	def press(self, btn=None, dir=None):
		self.format.setButton(btn)
		self.format.setDirection(dir)
		self.ser.writeRow(self.format.convert2str())
	
	def end(self):
		self.ser.writeRow('end')