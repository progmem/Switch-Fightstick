#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import serial


class Sender:
	def openSerial(self, portNum):
		self.ser = serial.Serial(portNum, 9600)
		
	def closeSerial(self):
		self.ser.close()
	
	def writeRow(self, row):
		self.ser.write((row+'\r\n').encode('utf-8'))
		print(row)
