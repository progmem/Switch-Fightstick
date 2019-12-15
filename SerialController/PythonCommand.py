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
			self.end(ser)
	
	def start(self, ser):
		if not self.thread:
			self.thread = threading.Thread(target=self.do_safe, args=([ser]))
			self.thread.start()
			self.started.set()
		self.keys = Keys.KeyPress(ser)

	def end(self, ser):
		ser.writeRow('end')
		self.keys = None
		self.started.clear()
		#self.thread.join()
		self.thread = None

	# press button at duration times(s)
	def press(self, button='', direction='', duration=0.1, wait=0.1):
		self.keys.press(Keys.Button(button), Keys.Direction(direction))
		self.wait(duration)
		self.keys.end()
		self.wait(wait)

	# do nothing at wait time(s)
	def wait(self, wait):
		sleep(wait)

	# press syntax sugars
	def pressBtn(self, btn, duration=0.1, wait=0.1):
		self.press(btn, '', duration, wait)

	def pressDir(self, dir, duration=0.1, wait=0.1):
		self.press('', dir, duration, wait)

	def pressBtnAndDir(self, btn, dir, duration=0.1, wait=0.1):
		self.press(btn, dir, duration, wait)
	

# Sync as controller
class Sync(PythonCommand):
	def __init__(self, name):
		super(Sync, self).__init__(name)
	
	def start(self, ser):
		super().start(ser)
	
	def do(self):
		self.wait(1)
		self.pressBtn('A', 0.1, 0.5)
		self.pressBtn('HOME', 0.1, 0.5)
		self.pressBtn('A', 0.1, 0.5)

		self.end()

# Unsync controller
class Unsync(PythonCommand):
	def __init__(self, name):
		super(Unsync, self).__init__(name)
	
	def do(self):
		self.wait(1)
		self.pressBtn('HOME', 0.1, 0.5)
		self.pressDir('LS DOWN', 0.1, 0.1)
		self.pressDir('LS RIGHT', 0.1, 0.1)
		self.pressDir('LS RIGHT', 0.1, 0.1)
		self.pressDir('LS RIGHT', 0.1, 0.1)
		self.pressBtn('A', 0.1, 1.5)
		self.pressBtn('A', 0.1, 0.5)
		self.pressBtn('A', 0.1, 0.3)

		self.end()

# Get watt automatically using the glitch
# source: MCU Command 'InifinityWatt'
class InfinityWatt(PythonCommand):
	def __init__(self, name):
		super(InfinityWatt, self).__init__(name)

	def do(self):
		while True:
			self.wait(1)

			self.pressBtn('A', wait=1)
			self.pressBtn('A', wait=3)	# レイド開始

			self.pressBtn('HOME', wait=1)
			self.pressDir('LS DOWN')
			self.pressDir('LS RIGHT')
			self.pressDir('LS RIGHT')
			self.pressDir('LS RIGHT')
			self.pressDir('LS RIGHT')
			self.pressBtn('A', wait=1.5) # 設定選択
			self.pressDir('LS DOWN', duration=2, wait=0.5)
			
			self.pressBtn('A', wait=0.3) # 設定 > 本体
			self.pressDir('LS DOWN')
			self.pressDir('LS DOWN')
			self.pressDir('LS DOWN')
			self.pressDir('LS DOWN')
			self.pressBtn('A') # 日付と時刻 選択
			self.pressBtn('A')

			self.pressDir('LS DOWN')
			self.pressDir('LS DOWN')
			self.pressBtn('A', wait=0.3)
			self.pressDir('LS UP', wait=0.3)
			self.pressDir('LS RIGHT', duration=1, wait=0.3)
			self.pressBtn('A')
			self.pressBtn('HOME', wait=0.3) # ゲームに戻る
			self.pressBtn('HOME', wait=0.3)
			
			self.pressBtn('B', wait=0.5)
			self.pressBtn('A', wait=3) # レイドをやめる

			self.pressBtn('A')
			self.pressBtn('A')
			self.pressBtn('B')
			self.pressBtn('B')

			self.pressBtn('HOME', wait=1)
			self.pressDir('LS DOWN')
			self.pressDir('LS RIGHT')
			self.pressDir('LS RIGHT')
			self.pressDir('LS RIGHT')
			self.pressDir('LS RIGHT')
			self.pressBtn('A', wait=1.5) # 設定選択
			self.pressDir('LS DOWN', duration=2, wait=0.5)
			
			self.pressBtn('A', wait=0.3) # 設定 > 本体
			self.pressDir('LS DOWN')
			self.pressDir('LS DOWN')
			self.pressDir('LS DOWN')
			self.pressDir('LS DOWN')
			self.pressBtn('A') # 日付と時刻 選択
			self.pressBtn('A')

			self.pressBtn('HOME', wait=0.3) # ゲームに戻る
			self.pressBtn('HOME', wait=0.3)


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
