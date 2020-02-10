#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ..PythonCommandBase import PythonCommand, ImageProcPythonCommand
from Commands.Keys import KeyPress, Button, Direction, Stick

# auto releaseing pokemons
class AutoRelease(ImageProcPythonCommand):
	NAME = '自動リリース'

	def __init__(self, cam):
		super().__init__(cam)
		self.row = 5
		self.col = 6
		self.cam = cam

	def do(self):
		self.wait(0.5)

		for i in range(0, self.row):
			for j in range(0, self.col):
				if not self.cam.isOpened():
					self.Release()
				else:
					# if shiny, then skip
					if not self.isContainTemplate('shiny_mark.png', threshold=0.9):
						if self.isContainTemplate('status.png', threshold=0.7): # Maybe this threshold works for only Japanese version.
							# Release a pokemon
							self.Release()


				if not j == self.col - 1:
					if i % 2 == 0:	self.press(Direction.RIGHT, wait=0.2)
					else:			self.press(Direction.LEFT, wait=0.2)

			self.press(Direction.DOWN, wait=0.2)

		# Return from pokemon box
		self.press(Button.B, wait=2)
		self.press(Button.B, wait=2)
		self.press(Button.B, wait=1.5)

	def Release(self):
		self.press(Button.A, wait=0.5)
		self.press(Direction.UP, wait=0.2)
		self.press(Direction.UP, wait=0.2)
		self.press(Button.A, wait=1)
		self.press(Direction.UP, wait=0.2)
		self.press(Button.A, wait=1.5)
		self.press(Button.A, wait=0.3)