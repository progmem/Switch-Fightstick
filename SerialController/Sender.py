#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import serial


class Sender:
	def openSerial(self, portNum):
		self.ser = serial.Serial(portNum, 9600)
		
	def closeSerial(self):
		self.ser.close()
	
	def pressKey(self, key):
		self.ser.write((key+'\r\n').encode('utf-8'))
		time.sleep(0.1)
	
	def writeRow(self, row):
		self.ser.write((row+'\r\n').encode('utf-8'))
		print(row)
		time.sleep(0.1)
