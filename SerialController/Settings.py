#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, json

class GuiSettings:
	SETTING_PATH = "./settings.json"

	def __init__(self):
		# default values
		self.camera_id = 0
		self.com_port = 0
		self.fps = 45
		self.is_show_realtime = True
		self.is_show_serial = False
		self.is_use_keyboard = True

	def load(self):
		if os.path.isfile(self.SETTING_PATH):
			load_settings = json.load(open(self.SETTING_PATH, 'r'))

			if self.__dict__.keys() != load_settings.keys():
				print('Setting items have been altered.')
				self.generate()
				self.load()
			else:
				self.__dict__ = load_settings
		else:
			print('No setting files can be found.')
			self.generate()
			self.load()

	def generate(self):
		self.save(path)
		print('A default settings file has been created.')

	def save(self, path=None):
		print(self.__dict__)
		json.dump(self.__dict__, open(self.SETTING_PATH if path is None else path, 'w'), indent=4)
