#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from time import sleep
from . import CommandBase
from .Keys import KeyPress, Button, Direction

# Sigle button command
class UnitCommand(CommandBase.Command):
	def __init__(self):
		super(UnitCommand, self).__init__()
	
	def start(self, ser, postProcess=None):
		self.isRunning = True
		self.key = KeyPress(ser)

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
	def __init__(self):
		super(A, self).__init__()

	def start(self, ser):
		super(A, self).start(ser)
		self.press(Button.A)

class B(UnitCommand):
	def __init__(self):
		super(B, self).__init__()

	def start(self, ser):
		super(B, self).start(ser)
		self.press(Button.B)

class X(UnitCommand):
	def __init__(self):
		super(X, self).__init__()

	def start(self, ser):
		super(X, self).start(ser)
		self.press(Button.X)

class Y(UnitCommand):
	def __init__(self):
		super(Y, self).__init__()

	def start(self, ser):
		super(Y, self).start(ser)
		self.press(Button.Y)

class L(UnitCommand):
	def __init__(self):
		super(L, self).__init__()

	def start(self, ser):
		super(L, self).start(ser)
		self.press(Button.L)

class R(UnitCommand):
	def __init__(self):
		super(R, self).__init__()

	def start(self, ser):
		super(R, self).start(ser)
		self.press(Button.R)

class ZL(UnitCommand):
	def __init__(self):
		super(ZL, self).__init__()

	def start(self, ser):
		super(ZL, self).start(ser)
		self.press(Button.ZL)

class ZR(UnitCommand):
	def __init__(self):
		super(ZR, self).__init__()

	def start(self, ser):
		super(ZR, self).start(ser)
		self.press(Button.ZR)

class MINUS(UnitCommand):
	def __init__(self):
		super(MINUS, self).__init__()

	def start(self, ser):
		super(MINUS, self).start(ser)
		self.press(Button.MINUS)

class PLUS(UnitCommand):
	def __init__(self):
		super(PLUS, self).__init__()

	def start(self, ser):
		super(PLUS, self).start(ser)
		self.press(Button.PLUS)

class LCLICK(UnitCommand):
	def __init__(self):
		super(LCLICK, self).__init__()

	def start(self, ser):
		super(LCLICK, self).start(ser)
		self.press(Button.LCLICK)

class RCLICK(UnitCommand):
	def __init__(self):
		super(RCLICK, self).__init__()

	def start(self, ser):
		super(RCLICK, self).start(ser)
		self.press(Button.RCLICK)

class HOME(UnitCommand):
	def __init__(self):
		super(HOME, self).__init__()

	def start(self, ser):
		super(HOME, self).start(ser)
		self.press(Button.HOME)

class CAPTURE(UnitCommand):
	def __init__(self):
		super(CAPTURE, self).__init__()

	def start(self, ser):
		super(CAPTURE, self).start(ser)
		self.press(Button.CAPTURE)

class UP(UnitCommand):
	def __init__(self):
		super(UP, self).__init__()

	def start(self, ser):
		super(UP, self).start(ser)
		self.press(Direction.UP)

class RIGHT(UnitCommand):
	def __init__(self):
		super(RIGHT, self).__init__()

	def start(self, ser):
		super(RIGHT, self).start(ser)
		self.press(Direction.RIGHT)

class DOWN(UnitCommand):
	def __init__(self):
		super(DOWN, self).__init__()

	def start(self, ser):
		super(DOWN, self).start(ser)
		self.press(Direction.DOWN)

class LEFT(UnitCommand):
	def __init__(self):
		super(LEFT, self).__init__()

	def start(self, ser):
		super(LEFT, self).start(ser)
		self.press(Direction.LEFT)
