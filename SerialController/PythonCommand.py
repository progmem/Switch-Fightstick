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
		self.alive = True
		self.postProcess = None
	
	@abstractclassmethod
	def do(self):
		pass

	def do_safe(self, ser):
		try:
			if self.alive:
				self.do()
		except:
			if not self.keys:
				self.keys = Keys.KeyPress(ser)
			print('interuppt')
			import traceback
			traceback.print_exc()
			self.keys.end()
			self.alive = False
	
	def start(self, ser, postProcess=None):
		self.alive = True
		self.postProcess = postProcess
		self.keys = Keys.KeyPress(ser)
		if not self.thread:
			self.thread = threading.Thread(target=self.do_safe, args=([ser]))
			self.thread.start()
		self.isRunning = True

	def end(self, ser):
		self.sendStopRequest()

	def sendStopRequest(self):
		if (self.checkIfAlive()): # try if we can stop now
			self.alive = False
			print (self.name + ': we\'ve sent a stop request.')
	
	# NOTE: Use this function if you want to get out from a command loop by yourself 
	def finish(self):
		self.alive = False
		self.end(self.keys.ser)

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
	def holdEnd(self, buttons):
		self.keys.holdEnd(buttons)

	# do nothing at wait time(s)
	def wait(self, wait):
		sleep(wait)
	
	def checkIfAlive(self):
		if (not self.alive):
			self.keys.end()
			self.keys = None
			self.thread = None
			self.isRunning = False
			print(self.name + ' has reached an alive check and exited succucesfully.')

			if not self.postProcess is None:
				self.postProcess()
				self.postProcess = None
			return False
		else:
			return True

# Python command using rank match glitch
class RankGlitchPythonCommand(PythonCommand):
	def __init__(self, name):
		super(RankGlitchPythonCommand, self).__init__(name)
		self.day = 0
	
	# Use time glitch 
	# Controls the system time and get every-other-day bonus without any punishments
	def timeLeap(self, is_go_back=True):
		self.press(Button.HOME, wait=1)
		self.press(Button.DOWN)
		self.press(Button.RIGHT)
		self.press(Button.RIGHT)
		self.press(Button.RIGHT)
		self.press(Button.RIGHT)
		self.press(Button.A, wait=1.5) # System Settings
		self.press(Button.DOWN, duration=2, wait=0.5)
		if not self.checkIfAlive(): return
		
		self.press(Button.A, wait=0.3) # System Settings > System
		self.press(Button.DOWN)
		self.press(Button.DOWN)
		self.press(Button.DOWN)
		self.press(Button.DOWN, wait=0.3)
		self.press(Button.A, wait=0.2) # Date and Time
		self.press(Button.DOWN, duration=0.7, wait=0.2)
		if not self.checkIfAlive(): return

		# increment and decrement
		if is_go_back:
			self.press(Button.A, wait=0.2)
			self.press(Button.UP, wait=0.2) # Increment a year
			self.press(Button.RIGHT, duration=1.5)
			self.press(Button.A, wait=0.5)
			if not self.checkIfAlive(): return

			self.press(Button.A, wait=0.2)
			self.press(Button.LEFT, duration=1.5)
			self.press(Button.DOWN, wait=0.2) # Decrement a year
			self.press(Button.RIGHT, duration=1.5)
			self.press(Button.A, wait=0.5)

		# use only increment
		# for use of faster time leap
		else:
			self.press(Button.A, wait=0.2)
			self.press(Button.RIGHT)
			self.press(Button.RIGHT)
			self.press(Button.UP, wait=0.2) # increment a day
			self.press(Button.RIGHT, duration=1)
			self.press(Button.A, wait=0.5)

		if not self.checkIfAlive(): return
		self.press(Button.HOME, wait=1)
		self.press(Button.HOME, wait=1)

# Sync as controller
# 同期
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
				
		self.finish()

# Unsync controller
# 同期解除
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

		self.finish()

# Mash a button A
# A連打
class Mash_A(PythonCommand):
	def __init__(self, name):
		super(Mash_A, self).__init__(name)

	def do(self):
		while self.checkIfAlive():
			self.wait(0.5)
			self.press(Button.A)

# using Rank Battle glitch
# Infinity ID lottery
# 無限IDくじ(ランクマッチ使用)
class InfinityLottery(RankGlitchPythonCommand):
	def __init__(self, name):
		super(InfinityLottery, self).__init__(name)

	def do(self):
		while self.checkIfAlive():
			self.press(Button.A, wait=0.5)
			self.press(Button.B, wait=0.5)
			self.press(Button.DOWN, wait=0.5)

			for _ in range(0, 10):	# A loop
				self.press(Button.A, wait=0.5)
				if not self.checkIfAlive(): return

			for _ in range(0, 20):  # B loop
				self.press(Button.B, wait=0.5)
				if not self.checkIfAlive(): return

			# Time glitch
			self.timeLeap()

# using RankBattle glitch
# Infinity getting berries
# 無限きのみ(ランクマッチ使用)
class InfinityBerry(RankGlitchPythonCommand):
	def __init__(self, name):
		super(InfinityBerry, self).__init__(name)
	
	def do(self):
		# As of now, we pick one berry every other day since excecuting without image recognition
		# 現在は画像認識使ってないので1回だけ取って終了
		while self.checkIfAlive():
			self.press(Button.A, wait=0.5)
			self.press(Button.B, wait=0.5)
			self.press(Button.A, wait=0.5) # yes

			for _ in range(0, 15):  # B loop
				self.press(Button.B, wait=0.5)
				if not self.checkIfAlive(): return

			# Time glitch
			self.timeLeap()

# for debug
class Move(PythonCommand):
	def __init__(self, name):
		super(Move, self).__init__(name)
	
	def do(self):
		while self.checkIfAlive():
			self.wait(1)

			# self.press(Button.PLUS, wait=1)
			# self.press(Button.DOWN, duration=0.3)
			# self.press(Button.LEFT, duration=2)
			# self.press(Button.UP, duration=2.1)
			# self.press(Button.RIGHT, duration=1, wait=2)

			self.press(Button.LEFT, duration=3)
			self.press(Button.UP, duration=4)
			self.press(Button.RIGHT, duration=1 ,wait=2)

			self.press(Button.DOWN, duration=1, wait=2)

			self.press(Button.X, wait=1)
			self.press(Button.A, wait=3) # open up a map
			self.press(Button.A, wait=1)
			self.press(Button.A, wait=4)
			self.press(Button.UP, duration=0.2)
			self.press([Button.UP, Button.LEFT], duration=1, wait=2)

			self.press(Button.DOWN, duration=1, wait=2)

# using RankBattle glitch
# Auto cafe battles
# 無限カフェ(ランクマッチ使用)
class InfinityCafe(RankGlitchPythonCommand):
	def __init__(self, name):
		super(InfinityCafe, self).__init__(name)
		self.pp_max = 10

	def do(self):
		while self.checkIfAlive():
			# battle agaist a master at PP times
			for __ in range(0, self.pp_max):
				self.wait(1)

				for _ in range(0, 35):	# A loop
					self.press(Button.A, wait=0.5)
					if not self.checkIfAlive(): return
				self.wait(5)

				for _ in range(0, 45):  # B loop
					self.press(Button.B, wait=0.5)
					if not self.checkIfAlive(): return
				
				self.timeLeap()
				if not self.checkIfAlive(): return
			
			# go to pokemon center to restore PP
			self.press(Button.DOWN, duration=3.5)
			self.press(Button.X, wait=1)
			self.press(Button.A, wait=3) # open up a map
			self.press(Button.A, wait=1)
			self.press(Button.A, wait=4)
			self.press(Button.UP, duration=0.2)
			self.press([Button.UP, Button.LEFT], duration=1, wait=2)

			# in pokemon center
			self.press(Button.UP, duration=2)
			for _ in range(0, 10):	# A loop
				self.press(Button.A, wait=0.5)
				if not self.checkIfAlive(): return
			for _ in range(0, 15):	# B loop
				self.press(Button.B, wait=0.5)
				if not self.checkIfAlive(): return
			self.press(Button.DOWN, duration=2, wait=2)
			if not self.checkIfAlive(): return

			# move to cafe in Wyndon (Shoot City)
			self.press(Button.LEFT, duration=3)
			self.press(Button.UP, duration=4)
			self.press(Button.RIGHT, duration=1 ,wait=2)
			if not self.checkIfAlive(): return

			self.press(Button.UP, duration=2, wait=1)


# auto egg hatching using image recognition
# 自動卵孵化(キャプボあり)
class AutoHatching(PythonCommand):
	def __init__(self, name):
		super(AutoHatching, self).__init__(name)

	def do(self):
		while self.checkIfAlive():
			self.wait(1)

# Get watt automatically using the glitch
# source: MCU Command 'InifinityWatt'
class InfinityWatt(RankGlitchPythonCommand):
	def __init__(self, name, is_use_rank):
		super(InfinityWatt, self).__init__(name)
		self.use_rank = is_use_rank

	def do(self):
		while self.checkIfAlive():
			self.wait(1)

			if self.use_rank:
				self.timeLeap()

				self.press(Button.A, wait=1)
				self.press(Button.A, wait=1) # 2000W
				self.press(Button.A, wait=1.8)
				self.press(Button.B, wait=1.5)

			else:
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

		while self.checkIfAlive():
			self.hold([Button.LEFT, Button.DOWN])
			self.wait(0.5)
			self.press(Button.X, wait=2)
			self.holdEnd([Button.LEFT, Button.DOWN])

			self.wait(1)

			self.hold(Button.UP)
			self.wait(2)

			self.holdEnd(Button.UP)
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
