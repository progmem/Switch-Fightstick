#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ..PythonCommandBase import PythonCommand, ImageProcPythonCommand
from Commands.Keys import KeyPress, Button, Direction, Stick

# Get watt automatically using the glitch
class InfinityWatt(PythonCommand):
	NAME = '無限ワット'

	def __init__(self):
		super().__init__()
		self.use_rank = True

	def do(self):
		while True:
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