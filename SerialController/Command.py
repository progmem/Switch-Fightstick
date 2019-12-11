#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractclassmethod
import Sender

class Command:
	__metaclass__ = ABCMeta

	def __init__(self, name):
		self.name = name
		self.ser = Sender.Sender()

	def getName(self):
		return self.name
	
	@abstractclassmethod
	def start(self):
		pass

	@abstractclassmethod
	def end(self):
		pass

# MCU command
# If you want to add extra commands, command enums in Joystick.c should also be rewritten.
class McuCommand(Command):
	def __init__(self, name):
		super(McuCommand, self).__init__(name)
		print('init MCU command: ' + name)
	
	def start(self):
		self.ser.writeRow(self.name)
	
	def end(self):
		self.ser.writeRow('end')

# Python command
class PythonCommand(Command):
	def __init__(self, name):
		super(PythonCommand, self).__init__(name)
		print('init Python command: ' + name)
	
	def start(self):
		pass

	def end(self):
		self.ser.writeRow('end')

class Sync(PythonCommand):
	def __init__(self, name):
		super(Sync, self).__init__(name)
	
	def start(self):
		pass
