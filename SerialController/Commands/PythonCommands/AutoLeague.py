#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ..PythonCommandBase import PythonCommand, ImageProcPythonCommand
from Commands.Keys import KeyPress, Button, Direction, Stick

# Auto league
# 自動リーグ周回(画像認識なし)
class AutoLeague(PythonCommand):
	NAME = '自動リーグ周回'

	def __init__(self):
		super().__init__()

	def do(self):
		self.hold(Direction(Stick.LEFT, 70))

		while True:
			for _ in range(0, 10):
				self.press(Button.A, wait=0.5)

			self.press(Button.B)