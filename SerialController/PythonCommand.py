#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractclassmethod
from time import sleep
import threading
import Command
import Keys
from Keys import Button

# Python command
class PythonCommand(Command.Command):
	def __init__(self, name):
		super(PythonCommand, self).__init__(name)
		print('init Python command: ' + name)
		self.keys = None
		self.thread = None
		self.started = threading.Event()
		self.alive = True
	
	@abstractclassmethod
	def do(self):
		pass

	def do_safe(self, ser):
		try:
			if (self.alive):
				self.do()
				self.started.wait()
		except:
			if (not self.keys):
				self.keys = Keys.KeyPress(ser)
			print('interuppt')
			import traceback
			traceback.print_exc()
			self.keys.end()
	
	def start(self, ser):
		if not self.thread:
			self.thread = threading.Thread(target=self.do_safe, args=([ser]))
			self.thread.start()
			self.started.set()
		self.keys = Keys.KeyPress(ser)

	# do not use this func. in commands
	# TODO: refactoring
	def end(self, ser):
		self.keys.end()
		self.keys = None
		self.started.clear()
		#self.thread.join()
		self.thread = None

	def endCommand(self):
		self.end('')

	# press button at duration times(s)
	def press(self, buttons, duration=0.1, wait=0.1):
		self.keys.input(buttons)
		self.wait(duration)
		self.keys.inputEnd(buttons)
		self.wait(wait)
	
	# add hold buttons
	def hold(self, buttons):
		self.keys.hold(buttons)
	
	# release holding buttons
	def endHold(self, buttons):
		self.keys.holdEnd(buttons)

	# do nothing at wait time(s)
	def wait(self, wait):
		sleep(wait)
	

# Sync as controller
class Sync(PythonCommand):
	def __init__(self, name):
		super(Sync, self).__init__(name)
	
	def start(self, ser):
		super().start(ser)
	
	def do(self):
		self.wait(1)

		self.press(Button.A, 0.1, 2)
		self.press(Button.HOME, 0.1, 1)
		self.press(Button.A, 0.1, 0.5)
				

		self.endCommand()

# Unsync controller
class Unsync(PythonCommand):
	def __init__(self, name):
		super(Unsync, self).__init__(name)
	
	def do(self):
		self.wait(1)
		self.press(Button.HOME, 0.1, 0.5)
		self.press(Button.DOWN, 0.1, 0.1)
		self.press(Button.RIGHT, 0.1, 0.1)
		self.press(Button.RIGHT, 0.1, 0.1)
		self.press(Button.RIGHT, 0.1, 0.1)
		self.press(Button.A, 0.1, 1.5)
		self.press(Button.A, 0.1, 0.5)
		self.press(Button.A, 0.1, 0.3)

		self.endCommand()


# Get watt automatically using the glitch
# source: MCU Command 'InifinityWatt'
class InfinityWatt(PythonCommand):
	def __init__(self, name):
		super(InfinityWatt, self).__init__(name)

	def do(self):
		while True:
			self.wait(1)

			self.press(Button.A, wait=1)
			self.press(Button.A, wait=3)	# レイド開始

			self.press(Button.HOME, wait=1)
			self.press(Button.DOWN)
			self.press(Button.RIGHT)
			self.press(Button.RIGHT)
			self.press(Button.RIGHT)
			self.press(Button.RIGHT)
			self.press(Button.A, wait=1.5) # 設定選択
			self.press(Button.DOWN, duration=2, wait=0.5)
			
			self.press(Button.A, wait=0.3) # 設定 > 本体
			self.press(Button.DOWN)
			self.press(Button.DOWN)
			self.press(Button.DOWN)
			self.press(Button.DOWN, wait=0.3)
			self.press(Button.A, wait=0.2) # 日付と時刻 選択
			self.press(Button.A, wait=0.4)

			self.press(Button.DOWN, wait=0.2)
			self.press(Button.DOWN, wait=0.2)
			self.press(Button.A, wait=0.2)
			self.press(Button.UP, wait=0.2)
			self.press(Button.RIGHT, duration=1, wait=0.3)
			self.press(Button.A, wait=0.5)
			self.press(Button.HOME, wait=1) # ゲームに戻る
			self.press(Button.HOME, wait=2)
			
			self.press(Button.B, wait=1)
			self.press(Button.A, wait=6) # レイドをやめる

			self.press(Button.A, wait=1)
			self.press(Button.A, wait=1) # 2000W
			self.press(Button.A, wait=1.8)
			self.press(Button.B, wait=1.5)

			self.press(Button.HOME, wait=1)
			self.press(Button.DOWN)
			self.press(Button.RIGHT)
			self.press(Button.RIGHT)
			self.press(Button.RIGHT)
			self.press(Button.RIGHT)
			self.press(Button.A, wait=1.5) # 設定選択
			self.press(Button.DOWN, duration=2, wait=0.5)
			
			self.press(Button.A, wait=0.3) # 設定 > 本体
			self.press(Button.DOWN)
			self.press(Button.DOWN)
			self.press(Button.DOWN)
			self.press(Button.DOWN)
			self.press(Button.A) # 日付と時刻 選択
			self.press(Button.A, wait=0.5)

			self.press(Button.HOME, wait=1) # ゲームに戻る
			self.press(Button.HOME, wait=1)

class HoldTest(PythonCommand):
	def __init__(self, name):
		super(HoldTest, self).__init__(name)

	def do(self):
		self.wait(1)

		while True:
			self.hold(Button.DOWN)
			self.wait(0.5)
			self.press(Button.X, wait=2)
			self.endHold(Button.DOWN)

			self.wait(1)

			self.hold(Button.UP)
			self.wait(2)

			self.endHold(Button.UP)
			self.wait(2)


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
