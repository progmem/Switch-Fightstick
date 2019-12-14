#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractclassmethod
from time import sleep
import threading
import Command
import Keys

# Python command
class PythonCommand(Command.Command):
	def __init__(self, name):
		super(PythonCommand, self).__init__(name)
		print('init Python command: ' + name)
		self.keys = None
		self.thread = None
	
	@abstractclassmethod
	def do(self):
		pass
	
	def start(self, ser):
		if not self.thread:
			self.thread = threading.Thread(target=self.do)
			self.thread.start()
		self.keys = Keys.KeyPress(ser)

	def end(self, ser):
		ser.writeRow('end')
		self.keys = None
		self.thread.join()
		self.thread = None

	# press button at duration times(s)
	def press(self, button, direction, duration, wait_time=0.1):
		try:
			self.keys.press(Keys.Buttons(button), Keys.Directions(direction))
			self.keys.end()
			self.wait(wait_time)
		except:
			pass # TODO: handle properly

	# do nothing at wait time(s)
	def wait(self, wait_time):
		sleep(wait_time)

	# press syntax sugars
	def pressButton(self, btn, duration=0.1, wait_time=0.1):
		self.press(btn, '', duration, wait_time)

	def pressDirection(self, dir, duration, wait_time=0.1):
		self.press('', dir, duration, wait_time)

	def pressButtonWithDirection(self, btn, dir, duration, wait_time=0.1):
		self.press(btn, dir, duration, wait_time)
	

# Sync as controller
class Sync(PythonCommand):
	def __init__(self, name):
		super(Sync, self).__init__(name)
	
	def start(self, ser):
		super().start(ser)
	
	def do(self):
		self.wait(1)
		self.pressButton('A', 0.1, 0.5)
		self.pressButton('HOME', 0.1, 0.5)
		self.pressButton('A', 0.1, 0.5)

# Unsync controller
class Unsync(PythonCommand):
	def __init__(self, name):
		super(Unsync, self).__init__(name)
	
	def do(self):
		self.wait(1)
		self.pressButton('HOME', 0.1, 0.5)
		self.pressDirection('L DOWN', 0.1, 0.1)
		self.pressDirection('L RIGHT', 0.1, 0.1)
		self.pressDirection('L RIGHT', 0.1, 0.1)
		self.pressDirection('L RIGHT', 0.1, 0.1)
		self.pressButton('A', 0.1, 1.5)
		self.pressButton('A', 0.1, 0.5)
		self.pressButton('A', 0.1, 0.3)


# sample initial code
# Copy and paste this class and write codes in start method.
# After you write the codes, don't forget to add commands list in Window.py.
# このクラスをコピぺしてstartメソッドの続きにコードを書いてください
# コードを書き終わったら, Window.pyのコマンド(self.py_command)に追加するのを忘れないように
class Sample(PythonCommand):
	def __init__(self, name):
		super(Sample, self).__init__(name)

	def do(self):
		self.wait(1)
