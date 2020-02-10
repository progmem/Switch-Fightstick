#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ..PythonCommandBase import PythonCommand, ImageProcPythonCommand
from Commands.Keys import KeyPress, Button, Direction, Stick

class Fossil_shiny(ImageProcPythonCommand):
	def __init__(self, cam):
		super().__init__(cam)

	'''
	head = {0 : "カセキのトリ", 1 : "カセキのサカナ"}
	body = {0 : "カセキのリュウ", 1 : "カセキのクビナガ"}
	'''
	def fossil_loop(self, head=0, body=0):
		# start = time.time()
		i = 0
		while True:
			for j in range(30):
				print(str(30*i+j+1)+"体目 ({}/30 of a box)".format(j+1))
				self.press(Button.A, wait=0.75)
				self.press(Button.A, wait=0.75)

				if head == 1:
					self.press(Direction.DOWN, duration=0.07, wait=0.75) # select fossil
				self.press(Button.A, wait=0.75) # determine fossil

				if body == 1:
					self.press(Direction.DOWN, duration=0.07, wait=0.75)  # select fossil
				self.press(Button.A, wait=0.75) # determine fossil

				self.press(Button.A, wait=0.75) # select "それでよければ"
				while not self.isContainTemplate('Network_Offline.png', 0.8):
					self.press(Button.B, wait=0.5)
				self.wait(1.0)

			# open up pokemon box
			self.press(Button.X, wait=1)
			self.press(Direction.RIGHT, duration=0.07, wait=1)
			self.press(Button.A, wait=2)
			self.press(Button.R, wait=2)

			is_contain_shiny = self.CheckBox()
			# tm = round(time.time() - start, 2)
			# print('Loop : {} in {} sec. Average: {} sec/loop'.format(i, tm, round(tm / i, 2)))
			if is_contain_shiny:
				print('Shiny!')
				break

			self.press(Button.HOME, wait=2)  # EXIT Game
			self.press(Button.X, wait=0.6)
			self.press(Button.A, wait=2.5)  # closed
			self.press(Button.A, wait=2.0)  # Choose game
			self.press(Button.A)  # User selection
			while not self.isContainTemplate('OP.png', 0.7): # recognize Opening
				self.wait(0.2)
			self.press(Button.A)  # load save-data
			while not self.isContainTemplate('Network_Offline.png', 0.8):
				self.wait(0.5)
			self.wait(1.0)
			i += 1

	def CheckBox(self):
		row = 5
		col = 6
		for i in range(0, row):
			for j in range(0, col):
				# if shiny, then stop
				if self.isContainTemplate('shiny_mark.png', threshold=0.9):
					return True
				# Maybe this threshold works for only Japanese version.
				if self.isContainTemplate('status.png', threshold=0.7):
					pass
				if not j == col - 1:
					if i % 2 == 0:
						self.press(Direction.RIGHT, wait=0.2)
					else:
						self.press(Direction.LEFT, wait=0.2)
			self.press(Direction.DOWN, wait=0.2)
		return False

class Fossil_shiny_00(Fossil_shiny): # パッチラゴン
	NAME = 'カセキ色厳選(パッチラゴン)'

	def __init__(self, cam):
		super().__init__(cam)

	def do(self):
		self.fossil_loop(0, 0)

class Fossil_shiny_01(Fossil_shiny): # パッチルドン
	NAME = 'カセキ色厳選(パッチルドン)'

	def __init__(self, cam):
		super().__init__(cam)

	def do(self):
		self.fossil_loop(0, 1)

class Fossil_shiny_10(Fossil_shiny): # ウオノラゴン
	NAME = 'カセキ色厳選(ウオノラゴン)'

	def __init__(self, cam):
		super().__init__(cam)

	def do(self):
		self.fossil_loop(1, 0)

class Fossil_shiny_11(Fossil_shiny): # ウオチルドン
	NAME = 'カセキ色厳選(ウオチルドン)'

	def __init__(self, cam):
		super().__init__(cam)

	def do(self):
		self.fossil_loop(1, 1)