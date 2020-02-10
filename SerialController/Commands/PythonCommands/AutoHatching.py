#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ..PythonCommandBase import PythonCommand, ImageProcPythonCommand
from Commands.Keys import KeyPress, Button, Direction, Stick

# auto egg hatching using image recognition
# 自動卵孵化(キャプボあり)
class AutoHatching(ImageProcPythonCommand):
	NAME = '自動卵孵化'

	def __init__(self, cam):
		super().__init__(cam)
		self.cam = cam
		self.party_num = 1	# don't count eggs
		self.hatched_num = 0
		self.hatched_box_num = 0
		self.itr_max = 6

	def do(self):
		self.press(Direction.DOWN, duration=0.05, wait=1)
		self.press(Direction.DOWN, duration=0.8)
		self.press(Direction.LEFT, duration=0.2)

		while True:
			for i in range(0, self.itr_max):
				print('iteration: ' + str(i+1) + ' (' + str(i*5) + '/30) -> (' + str((i+1)*5) + '/30)')
				print('hatched box num : ' + str(self.hatched_box_num))

				self.getNewEgg()
				self.press(Direction.UP, duration=0.05, wait=0.5)
				self.press(Direction.UP, duration=1)

				# hatch eggs
				while self.party_num < 6:
					self.press(Direction.RIGHT, duration=1)
					self.hold([Direction.RIGHT, Direction.R_LEFT])

					# turn round and round
					while not self.isContainTemplate('egg_notice.png'):
						self.wait(1)

					print('egg hatching')
					self.holdEnd([Direction.RIGHT, Direction.R_LEFT])
					self.press(Button.A)
					self.wait(15)
					for j in range(0, 5):
						self.press(Button.A, wait=1)
					self.hatched_num += 1
					self.party_num += 1
					print('party_num: ' + str(self.party_num))
					print('all hatched num: ' + str(self.hatched_num))

					self.press(Button.X, wait=1)
					self.press(Button.A, wait=3) # open up a map
					self.press(Button.A, wait=1)
					self.press(Button.A, wait=4)
					self.press(Direction.DOWN, duration=0.05, wait=0.5)
					self.press(Direction.DOWN, duration=0.8)
					self.press(Direction.LEFT, duration=0.2)

					if self.party_num < 6:
						# get a new egg
						self.getNewEgg()
						self.press(Direction.UP, duration=0.05, wait=0.5)
						self.press(Direction.UP, duration=1)

				# open up pokemon box
				self.press(Button.X, wait=1)
				self.press(Direction.RIGHT, wait=0.5) # set cursor to party
				self.press(Button.A, wait=2)
				self.press(Button.R, wait=2)

				self.putPokemonsToBox(start=1, num=5)
				self.party_num = 1

				if i < self.itr_max - 1:
					self.press(Button.B, wait=0.5)
					self.press(Button.B, wait=2)
					self.press(Button.B, wait=2)
					self.press(Direction.LEFT, wait=0.2) # set cursor to map
					self.press(Button.B, wait=1.5)

			self.hatched_box_num += 1

			# release
			self.press(Button.B, wait=0.8)
			self.press(Button.Y, wait=0.2)
			self.press(Direction.DOWN, wait=0.3)
			self.press(Direction.DOWN, wait=0.3)

			# As of now, stop if shiny is in box
			is_contain_shiny = self.ReleaseBox()
			if is_contain_shiny:
				print('shiny!')
				break

			self.press(Button.B, wait=0.5)
			self.press(Button.B, wait=2)
			self.press(Button.B, wait=2)
			self.press(Direction.LEFT, wait=0.2) # set cursor to map
			self.press(Button.B, wait=1.5)

	def getNewEgg(self):
		self.press(Button.A, wait=0.5)
		if not self.isContainTemplate('egg_found.png'):
			print('egg not found')
			self.finish() # TODO
		print('egg found')
		self.press(Button.A, wait=1)
		self.press(Button.A, wait=1)
		self.press(Button.A, wait=3)
		self.press(Button.A, wait=2)
		self.press(Button.A, wait=2)
		self.press(Button.A, wait=1)

	def putPokemonsToBox(self, start=0, num=1):
		self.press(Direction.LEFT, wait=0.3)
		self.pressRep(Direction.DOWN, start, wait=0.3)

		# select by range
		self.press(Button.Y, wait=0.2)
		self.press(Button.Y, wait=0.2)
		self.press(Button.A, wait=0.2)
		self.pressRep(Direction.DOWN, num-1)
		self.press(Button.A, wait=0.2)

		# put to box
		self.pressRep(Direction.UP, 3)
		self.press(Direction.RIGHT, wait=0.2)
		self.press(Button.A, wait=0.5)
		self.press(Button.A, wait=0.5)

	def ReleaseBox(self):
		row = 5
		col = 6
		for i in range(0, row):
			for j in range(0, col):

				# if shiny, then stop
				if self.isContainTemplate('shiny_mark.png', threshold=0.9):
					return True

				# Maybe this threshold works for only Japanese version.
				if self.isContainTemplate('status.png', threshold=0.7):
					# Release a pokemon
					self.Release()

				if not j == col - 1:
					if i % 2 == 0:	self.press(Direction.RIGHT, wait=0.2)
					else:			self.press(Direction.LEFT, wait=0.2)

			self.press(Direction.DOWN, wait=0.2)

		return False

	def Release(self):
		self.press(Button.A, wait=0.5)
		self.press(Direction.UP, wait=0.2)
		self.press(Direction.UP, wait=0.2)
		self.press(Button.A, wait=1)
		self.press(Direction.UP, wait=0.2)
		self.press(Button.A, wait=1.5)
		self.press(Button.A, wait=0.3)