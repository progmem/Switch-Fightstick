#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import Command

# MCU command
class McuCommand(Command.Command):
	def __init__(self, name, sync_name):
		super(McuCommand, self).__init__(name)
		print('init MCU command: ' + name)
		self.sync_name = sync_name
		self.postProcess = None
	
	def start(self, ser, postProcess):
		ser.writeRow(self.sync_name)
		self.isRunning = True
		self.postProcess = postProcess

	def end(self, ser):
		ser.writeRow('end')
		self.isRunning = False
		if not self.postProcess is None:
			self.postProcess()

# If you want to add extra commands, command enums in Joystick.c should also be rewritten.
class Mash_A(McuCommand):
	def __init__(self, name, sync_name = 'mash_a'):
		super(Mash_A, self).__init__(name, sync_name)

class AutoLeague(McuCommand):
	def __init__(self, name, sync_name = 'auto_league'):
		super(AutoLeague, self).__init__(name, sync_name)

class InfinityWatt(McuCommand):
	def __init__(self, name, sync_name = 'inf_watt'):
		super(InfinityWatt, self).__init__(name, sync_name)

class InfinityId(McuCommand):
	def __init__(self, name, sync_name = 'inf_id'):
		super(InfinityId, self).__init__(name, sync_name)

class Sync(McuCommand):
	def __init__(self, name, sync_name = 'sync'):
		super(Sync, self).__init__(name, sync_name)

class Unsync(McuCommand):
	def __init__(self, name, sync_name = 'unsync'):
		super(Unsync, self).__init__(name, sync_name)