import math
from collections import OrderedDict
from enum import IntEnum, Enum, auto

# Buttons and L stick directions
# As of now, we don't support HAT buttons though Joystick.c does.
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

	# for ease use of stick controls
	# L stick (not HAT)
	UP = 20
	RIGHT = auto()
	DOWN = auto()
	LEFT = auto()

	# R stick
	R_UP = auto()
	R_RIGHT = auto()
	R_DOWN = auto()
	R_LEFT = auto()

class Stick(Enum):
	LEFT = auto()
	RIGHT = auto()

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
	
	def resetAllButtons(self):
		self.format['btn'] = '00000000000000'

	def setDirection(self,  dirs):
		if Button.UP in dirs:		self.format['ly'] = min
		if Button.RIGHT in dirs:	self.format['lx'] = max
		if Button.DOWN in dirs:		self.format['ly'] = max
		if Button.LEFT in dirs:		self.format['lx'] = min
		if Button.R_UP in dirs:		self.format['ry'] = min
		if Button.R_RIGHT in dirs:	self.format['rx'] = max
		if Button.R_DOWN in dirs:	self.format['ry'] = max
		if Button.R_LEFT in dirs:	self.format['rx'] = min
	
	def setAnyDirection(self, dirs):
		for dir in dirs:
			if dir.stick == Stick.LEFT:
				self.format['lx'] = dir.x
				self.format['ly'] = 255 - dir.y # note that y axis direct under
			elif dir.stick == Stick.RIGHT:
				self.format['rx'] = dir.x
				self.format['ry'] = 255 - dir.y

	def unsetDirection(self, dirs):
		if Button.UP in dirs:		self.format['ly'] = center
		if Button.RIGHT in dirs:	self.format['lx'] = center
		if Button.DOWN in dirs:		self.format['ly'] = center
		if Button.LEFT in dirs:		self.format['lx'] = center
		if Button.R_UP in dirs:		self.format['ry'] = center
		if Button.R_RIGHT in dirs:	self.format['rx'] = center
		if Button.R_DOWN in dirs:	self.format['ry'] = center
		if Button.R_LEFT in dirs:	self.format['rx'] = micentern
	
	def resetAllDirections(self):
		self.format['lx'] = center
		self.format['ly'] = center
		self.format['rx'] = center
		self.format['ry'] = center

	def replacePartStr(self, str, add_str, index):
		return str[:index] + add_str + str[index+len(add_str):]

	def convert2str(self):
		str_format = ''
		for v in self.format.values():
			str_format += str(v)
			str_format += ' '
		return str_format[:-1] # the last space is not needed

# This class handle L stick and R stick at any angles
class Direction:
	def __init__(self, stick, angle, isDegree=True):
		stick_str = stick.upper()
		self.stick = None
		if stick_str == 'L':
			self.stick = Stick.LEFT
		elif stick_str == 'R':
			self.stick = Stick.RIGHT
		
		self.angle_for_show = angle
		angle = math.radians(angle) if isDegree else angle

		# We set stick X and Y from 0 to 255, so they are calculated as below.
		# X = 127.5*cos(theta) + 127.5
		# Y = 127.5*sin(theta) + 127.5
		self.x = math.ceil(127.5 * math.cos(angle) + 127.5)
		self.y = math.ceil(127.5 * math.sin(angle) + 127.5)

	def __repr__(self):
		return "Direction({}, {}[deg])".format(self.stick, self.angle_for_show)

	def __eq__(self, other):
		if (not type(other) is Direction):
			return False

		if self.stick == other.stick and self.angle_for_show == other.angle_for_show:
			return True
		else:
			return False

	def getTilting(self):
		tilting = []
		if self.stick == Stick.LEFT:
			if self.x < center:		tilting.append(Button.LEFT)
			elif self.x > center:	tilting.append(Button.RIGHT)

			if self.y < center:		tilting.append(Button.DOWN)
			elif self.y > center:	tilting.append(Button.UP)
		elif self.stick == Stick.RIGHT:
			if self.x < center:		tilting.append(Button.R_LEFT)
			elif self.x > center:	tilting.append(Button.R_RIGHT)

			if self.y < center:		tilting.append(Button.R_DOWN)
			elif self.y > center:	tilting.append(Button.R_UP)
		return tilting

# handles serial input to Joystick.c
class KeyPress:
	def __init__(self, ser):
		self.ser = ser
		self.format = SendFormat()
		self.holdButton = []
	
	def input(self, btns):
		if not isinstance(btns, list):
			btns = [btns]
		
		for btn in self.holdButton:
			if not btn in btns:
				btns.append(btn)

		# print to log
		print(btns)

		dirs = [btn for btn in btns if type(btn) is Direction]
		btns = [btn for btn in btns if type(btn) is Button]

		self.format.setAnyDirection(dirs)
		self.format.setButton([btn for btn in btns if int(btn) < BUTTON_NUM])
		self.format.setDirection(btns)
		self.ser.writeRow(self.format.convert2str())

	def inputEnd(self, btns):
		if not isinstance(btns, list):
			btns = [btns]

		dirs = [btn for btn in btns if type(btn) is Direction]
		btns = [btn for btn in btns if type(btn) is Button]

		# add direction from any angle
		for dir in dirs:
			tilts = dir.getTilting()
			for tilt in tilts:
				btns.append(tilt)

		self.format.unsetButton([btn for btn in btns if int(btn) < BUTTON_NUM])
		self.format.unsetDirection(btns)

		self.ser.writeRow(self.format.convert2str())

	def hold(self, btns):
		if not isinstance(btns, list):
			btns = [btns]

		for btn in btns:
			if btn in self.holdButton:
				print('Warning: ' + btn.name + ' is already in holding state')
				return
			
			self.holdButton.append(btn)
		
		self.input(btns)
		
	def holdEnd(self, btns):
		if not isinstance(btns, list):
			btns = [btns]
		
		for btn in btns:
			self.holdButton.remove(btn)

		self.inputEnd(btns)
	
	def end(self):
		self.ser.writeRow('end')