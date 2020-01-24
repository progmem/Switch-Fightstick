#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, os
import cv2
import time, datetime

class Camera:
	def __init__(self):
		self.camera = None
		self.capture_size = (1280, 720)
		self.capture_dir = "Captures"

	def openCamera(self, cameraId):
		if self.camera is not None and self.camera.isOpened():
			self.destroy()

		if os.name == 'nt':
			self.camera = cv2.VideoCapture(cameraId, cv2.CAP_DSHOW)
		else:
			self.camera = cv2.VideoCapture(cameraId)

		if not self.camera.isOpened():
			print("Camera ID " + str(cameraId) + " can't open.")
			return
		print("Camera ID " + str(cameraId) + " opened successfully")
		self.camera.set(cv2.CAP_PROP_FPS, 60)
		self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, self.capture_size[0])
		self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, self.capture_size[1])

	def isOpened(self):
		return self.camera.isOpened()

	def readFrame(self):
		_, self.image_bgr = self.camera.read()
		return self.image_bgr

	def saveCapture(self):
		dt_now = datetime.datetime.now()
		fileName = dt_now.strftime('%Y-%m-%d_%H-%M-%S')+".png"

		if not os.path.exists(self.capture_dir):
			os.makedirs(self.capture_dir)

		save_path = os.path.join(self.capture_dir, fileName)
		cv2.imwrite(save_path, self.image_bgr)
		print('capture succeeded: ' + save_path)
	
	def destroy(self):
		if self.camera is not None and self.camera.isOpened():
			self.camera.release()
			self.camera = None
