#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractclassmethod
from time import sleep
import threading
import Command
import Keys
import cv2
from Keys import Button, Direction, Stick
from Window import Camera

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
		self.press(Direction.DOWN)
		self.press(Direction.RIGHT)
		self.press(Direction.RIGHT)
		self.press(Direction.RIGHT)
		self.press(Direction.RIGHT)
		self.press(Button.A, wait=1.5) # System Settings
		self.press(Direction.DOWN, duration=2, wait=0.5)
		if not self.checkIfAlive(): return
		
		self.press(Button.A, wait=0.3) # System Settings > System
		self.press(Direction.DOWN)
		self.press(Direction.DOWN)
		self.press(Direction.DOWN)
		self.press(Direction.DOWN, wait=0.3)
		self.press(Button.A, wait=0.2) # Date and Time
		self.press(Direction.DOWN, duration=0.7, wait=0.2)
		if not self.checkIfAlive(): return

		# increment and decrement
		if is_go_back:
			self.press(Button.A, wait=0.2)
			self.press(Direction.UP, wait=0.2) # Increment a year
			self.press(Direction.RIGHT, duration=1.5)
			self.press(Button.A, wait=0.5)
			if not self.checkIfAlive(): return

			self.press(Button.A, wait=0.2)
			self.press(Direction.LEFT, duration=1.5)
			self.press(Direction.DOWN, wait=0.2) # Decrement a year
			self.press(Direction.RIGHT, duration=1.5)
			self.press(Button.A, wait=0.5)

		# use only increment
		# for use of faster time leap
		else:
			self.press(Button.A, wait=0.2)
			self.press(Direction.RIGHT)
			self.press(Direction.RIGHT)
			self.press(Direction.UP, wait=0.2) # increment a day
			self.press(Direction.RIGHT, duration=1)
			self.press(Button.A, wait=0.5)

		if not self.checkIfAlive(): return
		self.press(Button.HOME, wait=1)
		self.press(Button.HOME, wait=1)


TEMPLATE_PATH = "./Template/"
class ImageProcPythonCommand(PythonCommand):
	def __init__(self, name, cam):
		super(ImageProcPythonCommand, self).__init__(name)
		self.camera = cam
	
	# Judge if current screenshot contains an image using template matching
	# It's recommended that you use gray_scale option unless the template color wouldn't be cared for performace
	# 現在のスクリーンショットと指定した画像のテンプレートマッチングを行います
	# 色の違いを考慮しないのであればパフォーマンスの点からuse_grayをTrueにしてグレースケール画像を使うことを推奨します
	def isContainTemplate(self, template_path, threshold=0.7, use_gray=True, show_value=False):
		src = self.camera.readFrame()
		src = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY) if use_gray else src

		template = cv2.imread(TEMPLATE_PATH+template_path, cv2.IMREAD_GRAYSCALE if use_gray else cv2.IMREAD_COLOR)
		w, h = template.shape[1], template.shape[0]
		
		method = cv2.TM_CCOEFF_NORMED
		res = cv2.matchTemplate(src, template, method)
		_, max_val, _, max_loc = cv2.minMaxLoc(res)

		if show_value:
			print(template_path + ' ZNCC value: ' + str(max_val))

		if max_val > threshold:
			if use_gray:
				src = cv2.cvtColor(src, cv2.COLOR_GRAY2BGR)

			top_left = max_loc
			bottom_right = (top_left[0] + w, top_left[1] + h)
			cv2.rectangle(src, top_left, bottom_right, (255, 0, 255), 2)
			return True
		else:
			return False
	
	# Get interframe difference binarized image
	# フレーム間差分により2値化された画像を取得
	def getInterframeDiff(self, frame1, frame2, frame3, threshold):
		diff1 = cv2.absdiff(frame1, frame2)
		diff2 = cv2.absdiff(frame2, frame3)

		diff = cv2.bitwise_and(diff1, diff2)

		# binarize
		img_th = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)[1]

		# remove noise
		mask = cv2.medianBlur(img_th, 3)
		return mask


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
		self.press(Direction.DOWN, 0.1, 0.1)
		self.press(Direction.RIGHT, 0.1, 0.1)
		self.press(Direction.RIGHT, 0.1, 0.1)
		self.press(Direction.RIGHT, 0.1, 0.1)
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

# Auto league
# 自動リーグ周回(画像認識なし)
class AutoLeague(PythonCommand):
	def __init__(self, name):
		super(AutoLeague, self).__init__(name)

	def do(self):
		self.hold(Direction(Stick.LEFT, 70))
		while self.checkIfAlive():
			self.wait(0.5)

			for _ in range(0, 10):
				self.press(Button.A, wait=0.5)
			
			self.press(Button.B)

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
			self.press(Direction.DOWN, wait=0.5)

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
		# 画像認識使わない場合, 1回だけ取って終了
		while self.checkIfAlive():
			self.press(Button.A, wait=0.5)
			self.press(Button.B, wait=0.5)
			self.press(Button.A, wait=0.5) # yes

			for _ in range(0, 15):  # B loop
				self.press(Button.B, wait=0.5)
				if not self.checkIfAlive(): return

			# Time glitch
			self.timeLeap()

# using RankBattle glitch
# Infinity getting berries
# 無限きのみ(ランクマッチ, 画像認識使用)
class InfinityBerryIP(ImageProcPythonCommand, RankGlitchPythonCommand):
	def __init__(self, name, cam):
		super(InfinityBerryIP, self).__init__(name, cam)

	def do(self):
		while self.checkIfAlive():
			self.press(Button.A, wait=0.5)
			self.press(Button.B, wait=0.5)
			self.press(Button.A, wait=0.5) # yes

			while True:
				self.press(Button.A, wait=0.5) # for press 'shake more'
				self.press(Button.A, wait=0.5) # just in case
				self.press(Button.A, wait=0.5)

				while not self.isContainTemplate('fell_message.png'):
					self.press(Button.B, wait=0.5)
					if not self.checkIfAlive(): return
				print('fell message!')
				self.press(Button.A, wait=0.5)

				# Judge continuity by tree shaking motion
				if self.isContinue():
					print('continue')
					self.wait(0.5)
					continue
				else:
					print('not continue')
					break

			for _ in range(0, 10):  # B loop
				self.press(Button.B, wait=0.5)
				if not self.checkIfAlive(): return

			# Time glitch
			self.timeLeap()
	
	def isContinue(self, check_interval=0.1, check_duration=2):
		time = 0
		zero_cnt = 0
		height_half = int(self.camera.capture_size[1] / 2)

		frame1 = cv2.cvtColor(self.camera.readFrame()[0:height_half-1, :], cv2.COLOR_BGR2GRAY)
		sleep(check_interval / 3)
		frame2 = cv2.cvtColor(self.camera.readFrame()[0:height_half-1, :], cv2.COLOR_BGR2GRAY)
		sleep(check_interval / 3)
		frame3 = cv2.cvtColor(self.camera.readFrame()[0:height_half-1, :], cv2.COLOR_BGR2GRAY)
		
		while time < check_duration:
			mask = self.getInterframeDiff(frame1, frame2, frame3, 15)
			zero_cnt += cv2.countNonZero(mask)

			frame1 = frame2
			frame2 = frame3
			sleep(check_interval)
			frame3 = cv2.cvtColor(self.camera.readFrame()[0:height_half-1, :], cv2.COLOR_BGR2GRAY)

			time += check_interval
		
		print('diff cnt: ' + str(zero_cnt))

		# zero count threshold is heuristic value... weather: sunny
		return True if zero_cnt < 9000 else False


# for debug
class Move(PythonCommand):
	def __init__(self, name):
		super(Move, self).__init__(name)
	
	def do(self):
		self.hold([Direction(Stick.LEFT, 440), Direction(Stick.RIGHT, -60)])
		count = 0

		while self.checkIfAlive():
			self.wait(1)

			# self.press([Direction(Stick.LEFT, -60), Button.X], duration=1, wait=2)
			# self.press([Direction(Stick.LEFT, 275), Button.X], duration=1)

			#self.hold(Direction(Stick.LEFT, 120))
			self.press(Button.X, wait=1)

			count += 1
			if count > 1: 
				if (count == 2):
					self.holdEnd([Direction(Stick.LEFT, 440), Direction(Stick.RIGHT, -60)])

			#self.finish()


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
			self.press(Direction.DOWN, duration=3.5)
			self.press(Button.X, wait=1)
			self.press(Button.A, wait=3) # open up a map
			self.press(Button.A, wait=1)
			self.press(Button.A, wait=4)
			self.press(Direction.UP, duration=0.2)
			self.press([Direction.UP, Direction.LEFT], duration=1, wait=2)

			# in pokemon center
			self.press(Direction.UP, duration=2)
			for _ in range(0, 10):	# A loop
				self.press(Button.A, wait=0.5)
				if not self.checkIfAlive(): return
			for _ in range(0, 15):	# B loop
				self.press(Button.B, wait=0.5)
				if not self.checkIfAlive(): return
			self.press(Direction.DOWN, duration=2, wait=2)
			if not self.checkIfAlive(): return

			# move to cafe in Wyndon (Shoot City)
			self.press(Direction.LEFT, duration=3)
			self.press(Direction.UP, duration=4)
			self.press(Direction.RIGHT, duration=1 ,wait=2)
			if not self.checkIfAlive(): return

			self.press(Direction.UP, duration=2, wait=1)


# auto egg hatching using image recognition
# 自動卵孵化(キャプボあり)
class AutoHatching(ImageProcPythonCommand):
	def __init__(self, name, cam):
		super(AutoHatching, self).__init__(name, cam)

	def do(self):
		#self.wait(0.5)

		if self.isContainTemplate('baby_msg.png'):
			print('detected target box')

			for i in range(0, 5):
				for j in range(0, 6):
					# Maybe this threshold works for only Japanese version.
					# I'll consider the other way if needed.
					if self.isContainTemplate('milcery_status.png', threshold=0.4):
						# Release a pokemon
						self.press(Button.A, wait=0.5)
						self.press(Direction.UP, wait=0.2)
						self.press(Direction.UP, wait=0.2)
						self.press(Button.A, wait=1)
						self.press(Direction.UP, wait=0.2)
						self.press(Button.A, wait=1)
						self.press(Button.A, wait=0.3)
						if not self.checkIfAlive(): return
					
					if not j == 5:
						if i % 2 == 0:	self.press(Direction.RIGHT, wait=0.2)
						else:			self.press(Direction.LEFT, wait=0.2)
				
				self.press(Direction.DOWN, wait=0.2)

		# Return from pokemon box
		self.press(Button.B, wait=2)
		self.press(Button.B, wait=2)
		self.press(Button.B, wait=1.5)

		self.finish()

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
				self.press(Direction.DOWN)
				self.press(Direction.RIGHT)
				self.press(Direction.RIGHT)
				self.press(Direction.RIGHT)
				self.press(Direction.RIGHT)
				self.press(Button.A, wait=1.5) # 設定選択
				self.press(Direction.DOWN, duration=2, wait=0.5)
				
				self.press(Button.A, wait=0.3) # 設定 > 本体
				self.press(Direction.DOWN)
				self.press(Direction.DOWN)
				self.press(Direction.DOWN)
				self.press(Direction.DOWN, wait=0.3)
				self.press(Button.A, wait=0.2) # 日付と時刻 選択
				self.press(Button.A, wait=0.4)

				self.press(Direction.DOWN, wait=0.2)
				self.press(Direction.DOWN, wait=0.2)
				self.press(Button.A, wait=0.2)
				self.press(Direction.UP, wait=0.2)
				self.press(Direction.RIGHT, duration=1, wait=0.3)
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
				self.press(Direction.DOWN)
				self.press(Direction.RIGHT)
				self.press(Direction.RIGHT)
				self.press(Direction.RIGHT)
				self.press(Direction.RIGHT)
				self.press(Button.A, wait=1.5) # 設定選択
				self.press(Direction.DOWN, duration=2, wait=0.5)
				
				self.press(Button.A, wait=0.3) # 設定 > 本体
				self.press(Direction.DOWN)
				self.press(Direction.DOWN)
				self.press(Direction.DOWN)
				self.press(Direction.DOWN)
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
			self.hold([Direction.LEFT, Direction.DOWN])
			self.wait(0.5)
			self.press(Button.X, wait=2)
			self.holdEnd([Direction.LEFT, Direction.DOWN])

			self.wait(1)

			self.hold(Direction.UP)
			self.wait(2)

			self.holdEnd(Direction.UP)
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
