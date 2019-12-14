#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractclassmethod
import Sender

class Command:
	__metaclass__ = ABCMeta

	def __init__(self, name):
		self.name = name

	def getName(self):
		return self.name
	
	@abstractclassmethod
	def start(self, ser):
		pass

	@abstractclassmethod
	def end(self, ser):
		pass
