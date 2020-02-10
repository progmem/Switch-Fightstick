#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ..PythonCommandBase import PythonCommand, ImageProcPythonCommand
from Commands.Keys import KeyPress, Button, Direction, Stick

# Mash a button A
# A連打
class Mash_A(PythonCommand):
	NAME = 'A連打'

	def __init__(self):
		super().__init__()

	def do(self):
		while True:
			self.wait(0.5)
			self.press(Button.B)
