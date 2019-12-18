from collections import OrderedDict
from enum import IntEnum, auto

# Buttons and Directions
# As of now, we don't support R stick and HAT buttons though Joystick.c does.
class Button(IntEnum):
	A = 0
	B = auto()
	X = auto()
	Y = auto()
	L = auto()
	R = auto()
	ZL = auto()
	ZR = auto()
	MINUS = auto()
	PLUS = auto()
	LCLICK = auto()
	RCLICK = auto()
	HOME = auto()
	CAPTURE = auto()

	# L stick
	UP = 20
	RIGHT = auto()
	DOWN = auto()
	LEFT = auto()

BUTTON_NUM = int(Button.CAPTURE) + 1

# direction value definitions
min = 0
center = 128
max = 255

# serial format
class SendFormat:
	def __init__(self):
		# This format structure needs to be the same as the one written in Joystick.c
		self.format = OrderedDict([
			('cmd', 'p'),
			('btn', '00000000000000'),	# send bit array for buttons
			('lx', center),
			('ly', center),
			('rx', center),
			('ry', center),
			('hat', 8),
		])

	def setButton(self, btns):
		for btn in btns:
			self.format['btn'] = self.replacePartStr(self.format['btn'], '1', int(btn))
	
	def unsetButton(self, btns):
		for btn in btns:
			self.format['btn'] = self.replacePartStr(self.format['btn'], '0', int(btn))

	def setDirection(self, dirs):
		if (Button.UP in dirs):
			self.format['ly'] = min
		elif (Button.RIGHT in dirs):
			self.format['lx'] = max
		elif (Button.DOWN in dirs):
			self.format['ly'] = max
		elif (Button.LEFT in dirs):
			self.format['lx'] = min

	def unsetDirection(self, dirs):
		if (Button.UP in dirs):
			self.format['ly'] = center
		elif (Button.RIGHT in dirs):
			self.format['lx'] = center
		elif (Button.DOWN in dirs):
			self.format['ly'] = center
		elif (Button.LEFT in dirs):
			self.format['lx'] = center

	def replacePartStr(self, str, add_str, index):
		return str[:index] + add_str + str[index+len(add_str):]

	def convert2str(self):
		str_format = ''
		for v in self.format.values():
			str_format += str(v)
			str_format += ' '
		return str_format[:-1] # the last space is not needed


# handles serial input to Joystick.c
class KeyPress:
	def __init__(self, ser):
		self.ser = ser
		self.format = SendFormat()
		self.holdButton = []
	
	def input(self, btns):
		if (not isinstance(btns, list)):
			btns = [btns]
		
		for btn in self.holdButton:
			btns.append(btn)

		print(btns)

		self.format.setButton([btn for btn in btns if int(btn) < BUTTON_NUM])
		self.format.setDirection(btns)
		self.ser.writeRow(self.format.convert2str())

	def inputEnd(self, btns):
		if (not isinstance(btns, list)):
			btns = [btns]

		self.format.unsetButton(btns)
		self.format.unsetDirection(btns)

		self.ser.writeRow(self.format.convert2str())

	def hold(self, btns):
		if (not isinstance(btns, list)):
			btns = [btns]

		for btn in btns:
			if (btn in self.holdButton):
				print('Warning: ' + btn.name + ' is already in holding state')
				return
			
			self.holdButton.append(btn)
		
		self.input(btns)
		
	def holdEnd(self, btns):
		if (not isinstance(btns, list)):
			btns = [btns]
		
		for btn in btns:
			self.holdButton.remove(btn)

		self.inputEnd(btns)
	
	def end(self):
		self.ser.writeRow('end')