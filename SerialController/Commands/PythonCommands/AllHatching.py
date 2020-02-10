#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ..PythonCommandBase import PythonCommand, ImageProcPythonCommand
from Commands.Keys import KeyPress, Button, Direction, Stick

# Egg hatching at count times
# すべての孵化(キャプボあり)
# 現在は手持ちのみ
class AllHatching(ImageProcPythonCommand):
	NAME = '全卵孵化'

	def __init__(self, cam):
		super().__init__(cam)
		self.hatched_num = 0
		self.count = 5
		self.place = 'wild_area'

	def do(self):
		while self.hatched_num < self.count:
			if self.hatched_num == 0:
				self.press(Direction.RIGHT, duration=1)

			self.hold([Direction.RIGHT, Direction.R_LEFT])

			# turn round and round
			while not self.isContainTemplate('egg_notice.png'):
				self.wait(1)

			print('egg hatching')
			self.holdEnd([Direction.RIGHT, Direction.R_LEFT])
			self.press(Button.A)
			self.wait(15)
			for i in range(0, 5):
				self.press(Button.A, wait=1)
			self.hatched_num += 1
			print('hatched_num: ' + str(self.hatched_num))