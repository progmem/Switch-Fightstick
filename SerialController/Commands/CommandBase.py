#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractclassmethod
from . import Sender

class Command:
	__metaclass__ = ABCMeta

	def __init__(self):
		self.isRunning = False

	@abstractclassmethod
	def start(self, ser, postProcess=None):
		pass

	@abstractclassmethod
	def end(self, ser):
		pass
