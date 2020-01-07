#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import serial


class Sender:
	def __init__(self):
		self.ser = None
		self.is_show_serial = False

	def openSerial(self, portNum):
		self.ser = serial.Serial(portNum, 9600)
		
	def closeSerial(self):
		self.ser.close()
	
	def isOpened(self):
		return not self.ser is None and self.ser.isOpen()
	
	def setIsShowSerial(self, is_show):
		self.is_show_serial = is_show

	def writeRow(self, row):
		self.ser.write((row+'\r\n').encode('utf-8'))

		# Show sending serial datas
		if self.is_show_serial:
			print(row)
