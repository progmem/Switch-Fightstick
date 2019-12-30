#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from time import sleep
import Command
import Keys
from Keys import Button, Direction

# Sigle button command
class UnitCommand(Command.Command):
	def __init__(self, name=None):
		if name is None:
			name = self.__class__.__name__
		super(UnitCommand, self).__init__(name)
	
	def start(self, ser, postProcess=None):
		self.isRunning = True
		self.key = Keys.KeyPress(ser)

	def end(self, ser):
		pass

	# do nothing at wait time(s)
	def wait(self, wait):
		sleep(wait)
	
	def press(self, btn):
		self.key.input([btn])
		self.wait(0.1)
		self.key.inputEnd([btn])
		self.isRunning = False
		self.key = None

class A(UnitCommand):
	def __init__(self, name=None):
		super(A, self).__init__(name)

	def start(self, ser):
		super(A, self).start(ser)
		self.press(Button.A)

class B(UnitCommand):
	def __init__(self, name=None):
		super(B, self).__init__(name)

	def start(self, ser):
		super(B, self).start(ser)
		self.press(Button.B)

class X(UnitCommand):
	def __init__(self, name=None):
		super(X, self).__init__(name)

	def start(self, ser):
		super(X, self).start(ser)
		self.press(Button.X)

class Y(UnitCommand):
	def __init__(self, name=None):
		super(Y, self).__init__(name)

	def start(self, ser):
		super(Y, self).start(ser)
		self.press(Button.Y)

class L(UnitCommand):
	def __init__(self, name=None):
		super(L, self).__init__(name)

	def start(self, ser):
		super(L, self).start(ser)
		self.press(Button.L)

class R(UnitCommand):
	def __init__(self, name=None):
		super(R, self).__init__(name)

	def start(self, ser):
		super(R, self).start(ser)
		self.press(Button.R)

class ZL(UnitCommand):
	def __init__(self, name=None):
		super(ZL, self).__init__(name)

	def start(self, ser):
		super(ZL, self).start(ser)
		self.press(Button.ZL)

class ZR(UnitCommand):
	def __init__(self, name=None):
		super(ZR, self).__init__(name)

	def start(self, ser):
		super(ZR, self).start(ser)
		self.press(Button.ZR)

class MINUS(UnitCommand):
	def __init__(self, name=None):
		super(MINUS, self).__init__(name)

	def start(self, ser):
		super(MINUS, self).start(ser)
		self.press(Button.MINUS)

class PLUS(UnitCommand):
	def __init__(self, name=None):
		super(PLUS, self).__init__(name)

	def start(self, ser):
		super(PLUS, self).start(ser)
		self.press(Button.PLUS)

class LCLICK(UnitCommand):
	def __init__(self, name=None):
		super(LCLICK, self).__init__(name)

	def start(self, ser):
		super(LCLICK, self).start(ser)
		self.press(Button.LCLICK)

class RCLICK(UnitCommand):
	def __init__(self, name=None):
		super(RCLICK, self).__init__(name)

	def start(self, ser):
		super(RCLICK, self).start(ser)
		self.press(Button.RCLICK)

class HOME(UnitCommand):
	def __init__(self, name=None):
		super(HOME, self).__init__(name)

	def start(self, ser):
		super(HOME, self).start(ser)
		self.press(Button.HOME)

class CAPTURE(UnitCommand):
	def __init__(self, name=None):
		super(CAPTURE, self).__init__(name)

	def start(self, ser):
		super(CAPTURE, self).start(ser)
		self.press(Button.CAPTURE)


class UnitDirectionCommand(UnitCommand):
	def __init__(self, name=None):
		super(UnitDirectionCommand, self).__init__(name)
		self.toggle = False

	def start(self, ser):
		self.isRunning = True
		self.toggle = not self.toggle
		self.key = Keys.KeyPress(ser)
	
	def press(self, btn):
		if self.toggle:
			self.key.input([btn])
		else:
			self.key.inputEnd([btn])
		self.isRunning = False
		self.key = None

class UP(UnitDirectionCommand):
	def __init__(self, name=None):
		super(UP, self).__init__(name)

	def start(self, ser):
		super(UP, self).start(ser)
		self.press(Direction.UP)

class RIGHT(UnitDirectionCommand):
	def __init__(self, name=None):
		super(RIGHT, self).__init__(name)

	def start(self, ser):
		super(RIGHT, self).start(ser)
		self.press(Direction.RIGHT)

class DOWN(UnitDirectionCommand):
	def __init__(self, name=None):
		super(DOWN, self).__init__(name)

	def start(self, ser):
		super(DOWN, self).start(ser)
		self.press(Direction.DOWN)

class LEFT(UnitDirectionCommand):
	def __init__(self, name=None):
		super(LEFT, self).__init__(name)

	def start(self, ser):
		super(LEFT, self).start(ser)
		self.press(Direction.LEFT)