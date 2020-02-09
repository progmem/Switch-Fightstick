#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import serial

class Sender:
	def __init__(self, is_show_serial):
		self.ser = None
		self.is_show_serial = is_show_serial

	def openSerial(self, portNum):
		try:
			if os.name == 'nt':
				print('connecting to ' + "COM" + str(portNum))
				self.ser = serial.Serial("COM" + str(portNum), 9600)
				return True
			elif os.name == 'posix':
				print('connecting to ' + "/dev/ttyUSB" + str(portNum))
				self.ser = serial.Serial("/dev/ttyUSB" + str(portNum), 9600)
				return True
			else:
				print('not supported OS')
				return False
		except IOError:
			print('COM Port: can\'t be established')
			import traceback
			traceback.print_exc()
			return False
				
	def closeSerial(self):
		self.ser.close()
	
	def isOpened(self):
		return not self.ser is None and self.ser.isOpen()

	def writeRow(self, row):
		try:
			self.ser.write((row+'\r\n').encode('utf-8'))
		except serial.serialutil.SerialException as e:
			print(e)

		# Show sending serial datas
		if self.is_show_serial.get():
			print(row)
