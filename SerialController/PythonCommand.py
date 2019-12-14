#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from time import sleep
import Command
import Keys

# Python command
class PythonCommand(Command.Command):
	def __init__(self, name):
		super(PythonCommand, self).__init__(name)
		print('init Python command: ' + name)
		self.keys = None
	
	def start(self, ser):
		self.keys = Keys.KeyPress(ser)

	def end(self, ser):
		ser.writeRow('end')
		self.keys = None

	# press button at duration times(s)
	def press(self, button, direction, duration, wait_time=0.1):
		self.keys.press(Keys.Buttons(button), Keys.Directions(direction))
		self.keys.end()
		self.wait(wait_time)

	# do nothing at wait time(s)
	def wait(self, wait_time):
		sleep(wait_time)

	# press syntax sugars
	def pressButton(self, btn, duration, wait_time=0.1):
		self.press(btn, '', duration, wait_time)

	def pressDirection(self, dir, button, duration, wait_time=0.1):
		self.press('', dir, duration, wait_time)

	def pressButtonWithDirection(self, btn, dir, duration, wait_time=0.1):
		self.press(btn, dir, duration, wait_time)
	

# Sync as controller
class Sync(PythonCommand):
	def __init__(self, name):
		super(Sync, self).__init__(name)
	
	def start(self, ser):
		super().start(ser)

		self.wait(1)
		self.pressButton('A', 0.1, 0.5)
		self.pressButton('HOME', 0.1, 0.5)
		self.pressButton('A', 0.1, 0.5)

# Unsync controller
class Unsync(PythonCommand):
	def __init__(self, name):
		super(Unsync, self).__init__(name)
	
	def start(self, ser):
		super().start(self, ser)