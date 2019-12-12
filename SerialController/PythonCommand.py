#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import Command

# Python command
class PythonCommand(Command.Command):
	def __init__(self, name):
		super(PythonCommand, self).__init__(name)
		print('init Python command: ' + name)
	
	def start(self, ser):
		pass

	def end(self, ser):
		ser.writeRow('end')

class Sync(PythonCommand):
	def __init__(self, name):
		super(Sync, self).__init__(name)
	
	def start(self):
		pass
