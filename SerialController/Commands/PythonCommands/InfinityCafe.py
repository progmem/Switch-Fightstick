#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ..PythonCommandBase import PythonCommand, ImageProcPythonCommand
from Commands.Keys import KeyPress, Button, Direction, Stick

# using RankBattle glitch
# Auto cafe battles
# 無限カフェ(ランクマッチ使用)
class InfinityCafe(PythonCommand):
	NAME = '無限カフェ'

	def __init__(self):
		super().__init__()
		self.pp_max = 10

	def do(self):
		while True:
			# battle agaist a master at PP times
			for __ in range(0, self.pp_max):
				self.wait(1)

				for _ in range(0, 35):	# A loop
					self.press(Button.A, wait=0.5)
				self.wait(5)

				for _ in range(0, 45):  # B loop
					self.press(Button.B, wait=0.5)

				self.timeLeap()

			# go to pokemon center to restore PP
			self.press(Direction.DOWN, duration=3.5)
			self.press(Button.X, wait=1)
			self.press(Button.A, wait=3) # open up a map
			self.press(Button.A, wait=1)
			self.press(Button.A, wait=4)
			self.press(Direction.UP, duration=0.2)
			self.press(Direction.UP_LEFT, duration=1, wait=2)

			# in pokemon center
			self.press(Direction.UP, duration=2)
			for _ in range(0, 10):	# A loop
				self.press(Button.A, wait=0.5)
			for _ in range(0, 15):	# B loop
				self.press(Button.B, wait=0.5)
			self.press(Direction.DOWN, duration=2, wait=2)

			# move to cafe in Wyndon (Shoot City)
			self.press(Direction.LEFT, duration=3)
			self.press(Direction.UP, duration=4)
			self.press(Direction.RIGHT, duration=1 ,wait=2)

			self.press(Direction.UP, duration=2, wait=1)