#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ..PythonCommandBase import PythonCommand, ImageProcPythonCommand
from Commands.Keys import KeyPress, Button, Direction, Stick

class InfinityFeather(PythonCommand):
	NAME = '無限羽回収'

	def __init__(self):
		super().__init__()

	def do(self):
		# 時間等確認用。使用する際は "import time" すること
		# start = time.time()
		# i = 0  # カウンタ
		print('Start collecting feathers')
		while True:
			self.wait(0.75)
			# i += 1
			# print('Map')
			self.press(Button.X, wait=1.5) # open up a map
			self.press(Button.A, wait=3.0)
			self.press(Direction(Stick.LEFT, 45), duration=0.05) # Select a Pokémon Day Care
			self.press(Button.A, wait=1)
			self.press(Button.A, wait=4.0)

			# print('pick feather')
			self.press(Direction.DOWN_RIGHT, duration=0.15)
			self.press(Direction.RIGHT, duration=3)
			self.press(Button.A, wait=0.3)
			self.press(Button.A, wait=0.3)
			self.press(Button.A, wait=0.3)
			self.press(Button.A, wait=0.3)

			# print('Time leap')
			self.timeLeap()
			# tm = round(time.time() - start, 2)
			# print('Loop : {} in {} sec. Average: {} sec/loop'.format(i, tm, round(tm / i, 2)))