#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math
from collections import OrderedDict
from enum import IntFlag, Enum, auto

# Buttons and L stick directions
# As of now, we don't support HAT buttons though Joystick.c does.
class Button(IntFlag):
	Y = auto()
	B = auto()
	A = auto()
	X = auto()
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

class Stick(Enum):
	LEFT = auto()
	RIGHT = auto()

class Tilt(Enum):
	UP = auto()
	RIGHT = auto()
	DOWN = auto()
	LEFT = auto()
	R_UP = auto()
	R_RIGHT = auto()
	R_DOWN = auto()
	R_LEFT = auto()

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
			('btn', 0),	# send bit array for buttons
			('lx', center),
			('ly', center),
			('rx', center),
			('ry', center),
			('hat', 8),
		])

		self.L_stick_changed = False
		self.R_stick_changed = False

	def setButton(self, btns):
		for btn in btns:
			self.format['btn'] |= btn
	
	def unsetButton(self, btns):
		for btn in btns:
			self.format['btn'] &= ~btn
	
	def resetAllButtons(self):
		self.format['btn'] = 0
	
	def setAnyDirection(self, dirs):
		for dir in dirs:
			if dir.stick == Stick.LEFT:
				if self.format['lx'] != dir.x or self.format['ly'] != 255 - dir.y:
					self.L_stick_changed = True

				self.format['lx'] = dir.x
				self.format['ly'] = 255 - dir.y # NOTE: y axis directs under
			elif dir.stick == Stick.RIGHT:
				if self.format['rx'] != dir.x or self.format['ry'] != 255 - dir.y:
					self.R_stick_changed = True

				self.format['rx'] = dir.x
				self.format['ry'] = 255 - dir.y

	def unsetDirection(self, dirs):
		if Tilt.UP in dirs or Tilt.DOWN in dirs:
			self.format['ly'] = center
			self.format['lx'] = self.fixOtherAxis(self.format['lx'])
			self.L_stick_changed = True
		if Tilt.RIGHT in dirs or Tilt.LEFT in dirs:
			self.format['lx'] = center
			self.format['ly'] = self.fixOtherAxis(self.format['ly'])
			self.L_stick_changed = True
		if Tilt.R_UP in dirs or Tilt.R_DOWN in dirs:
			self.format['ry'] = center
			self.format['rx'] = self.fixOtherAxis(self.format['rx'])
			self.R_stick_changed = True
		if Tilt.R_RIGHT in dirs or Tilt.R_LEFT in dirs:
			self.format['rx'] = center
			self.format['ry'] = self.fixOtherAxis(self.format['ry'])
			self.R_stick_changed = True
	
	# Use this to fix an either tilt to max when the other axis sets to 0
	def fixOtherAxis(self, fix_target):
		if fix_target == center:
			return center
		else:
			return 0 if fix_target < center else 255
	
	def resetAllDirections(self):
		self.format['lx'] = center
		self.format['ly'] = center
		self.format['rx'] = center
		self.format['ry'] = center
		self.L_stick_changed = True
		self.R_stick_changed = True

	def convert2str(self):
		str_format = ''
		str_L = ''
		str_R = ''
		space = ' '

		# set bits array with stick flags
		send_btn = int(self.format['btn']) << 2
		if self.L_stick_changed:
			send_btn |= 0x2
			str_L = format(self.format['lx'], 'x') + space + format(self.format['ly'], 'x')
		if self.R_stick_changed:
			send_btn |= 0x1
			str_R = format(self.format['rx'], 'x') + space + format(self.format['ry'], 'x')

		str_format = self.format['cmd'] + space + format(send_btn, 'x') +\
			(space + str_L if self.L_stick_changed else '') +\
			(space + str_R if self.R_stick_changed else '')

		self.L_stick_changed = False
		self.R_stick_changed = False

		return str_format # the last space is not needed

# This class handle L stick and R stick at any angles
class Direction:
	def __init__(self, stick, angle, isDegree=True, showName=None):
		self.stick = stick	
		self.angle_for_show = angle
		self.showName = showName
		angle = math.radians(angle) if isDegree else angle

		# We set stick X and Y from 0 to 255, so they are calculated as below.
		# X = 127.5*cos(theta) + 127.5
		# Y = 127.5*sin(theta) + 127.5
		self.x = math.ceil(127.5 * math.cos(angle) + 127.5)
		self.y = math.floor(127.5 * math.sin(angle) + 127.5)

	def __repr__(self):
		if self.showName:
			return "<{}, {}>".format(self.stick, self.showName)
		else:
			return "<{}, {}[deg]>".format(self.stick, self.angle_for_show)

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
			if self.x < center:		tilting.append(Tilt.LEFT)
			elif self.x > center:	tilting.append(Tilt.RIGHT)

			if self.y < center-1:	tilting.append(Tilt.DOWN)
			elif self.y > center-1:	tilting.append(Tilt.UP)
		elif self.stick == Stick.RIGHT:
			if self.x < center:		tilting.append(Tilt.R_LEFT)
			elif self.x > center:	tilting.append(Tilt.R_RIGHT)

			if self.y < center-1:	tilting.append(Tilt.R_DOWN)
			elif self.y > center-1:	tilting.append(Tilt.R_UP)
		return tilting

# Left stick for ease of use
Direction.UP = Direction(Stick.LEFT, 90, showName='UP')
Direction.RIGHT = Direction(Stick.LEFT, 0, showName='RIGHT')
Direction.DOWN = Direction(Stick.LEFT, -90, showName='DOWN')
Direction.LEFT = Direction(Stick.LEFT, -180, showName='LEFT')
Direction.UP_RIGHT = Direction(Stick.LEFT, 45, showName='UP_RIGHT')
Direction.DOWN_RIGHT = Direction(Stick.LEFT, -45, showName='DOWN_RIGHT')
Direction.DOWN_LEFT = Direction(Stick.LEFT, -135, showName='DOWN_LEFT')
Direction.UP_LEFT = Direction(Stick.LEFT, 135, showName='UP_LEFT')
# Right stick for ease of use
Direction.R_UP = Direction(Stick.RIGHT, 90, showName='UP')
Direction.R_RIGHT = Direction(Stick.RIGHT, 0, showName='RIGHT')
Direction.R_DOWN = Direction(Stick.RIGHT, -90, showName='DOWN')
Direction.R_LEFT = Direction(Stick.RIGHT, -180, showName='LEFT')
Direction.R_UP_RIGHT = Direction(Stick.RIGHT, 45, showName='UP_RIGHT')
Direction.R_DOWN_RIGHT = Direction(Stick.RIGHT, -45, showName='DOWN_RIGHT')
Direction.R_DOWN_LEFT = Direction(Stick.RIGHT, -135, showName='DOWN_LEFT')
Direction.R_UP_LEFT = Direction(Stick.RIGHT, 135, showName='UP_LEFT')

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

		self.format.setButton([btn for btn in btns if type(btn) is Button])
		self.format.setAnyDirection([btn for btn in btns if type(btn) is Direction])
		self.ser.writeRow(self.format.convert2str())

	def inputEnd(self, btns):
		if not isinstance(btns, list):
			btns = [btns]

		# get tilting direction from angles
		tilts = []
		for dir in [btn for btn in btns if type(btn) is Direction]:
			tiltings = dir.getTilting()
			for tilting in tiltings:
				tilts.append(tilting)

		self.format.unsetButton([btn for btn in btns if type(btn) is Button])
		self.format.unsetDirection(tilts)

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