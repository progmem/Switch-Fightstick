#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from tkinter.scrolledtext import ScrolledText
import tkinter as tk
from tkinter import ttk
import cv2
from PIL import Image,ImageTk
import time
import datetime
import Command

DEFAULT_CAMERA_ID = 0
DEFAULT_COM_PORT = 8

# To avoid the error says 'ScrolledText' object has no attribute 'flush'
class MyScrolledText(ScrolledText):
	def flush(self):
		pass

class CAMERA:
	def __init__(self):
		self.camera=None
		
	def openCamera(self, cameraId):
		if self.camera is not None and self.camera.isOpened():
			self.camera.release()
			self.camera = None
		self.camera = cv2.VideoCapture(1 + cv2.CAP_DSHOW)
		if not self.camera.isOpened():
			print("Camera ID: " + str(cameraId) + " can't open.")
			return
		self.camera.set(cv2.CAP_PROP_FPS, 30)
		self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
		self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
	
	def readFrame(self):
		_, self.image_bgr = self.camera.read()
		return self.image_bgr
	
	def saveCapture(self):
		dt_now = datetime.datetime.now()
		fileName = dt_now.strftime('%Y-%m-%d_%H-%M-%S')+".png"
		cv2.imwrite(fileName, self.image_bgr)

class GUI:
	def __init__(self):
		self.autoPlayer = None
		
		self.root = tk.Tk()
		self.root.title('Pokemon Sword and Shield Auto Playing')
		self.frame1 = ttk.Frame(
			self.root,
			height=720,
			width=1280,
			relief='flat',
			borderwidth=5)
			
		self.label1 = ttk.Label(self.frame1, text='Camera ID:')
		self.cameraID = tk.IntVar()
		self.cameraID.set(DEFAULT_CAMERA_ID)
		self.entry1 = ttk.Entry(self.frame1, width=5, textvariable=self.cameraID)

		self.showPreview = tk.BooleanVar()
		self.showPreview.set(False)
		self.cb1 = ttk.Checkbutton(
			self.frame1,
			padding=5,
			text='Show Preview',
			onvalue=True,
			offvalue=False,
			variable=self.showPreview)
		self.showPreview.set(True)
		
		self.label2 = ttk.Label(self.frame1, text='COM Port:')
		self.comPort = tk.IntVar()
		self.comPort.set(DEFAULT_COM_PORT)
		self.entry2 = ttk.Entry(self.frame1, width=5, textvariable=self.comPort)

		self.preview = ttk.Label(self.frame1) 

		self.reloadButton = ttk.Button(self.frame1, text='Reload Camera', command=self.openCamera)
		self.startButton = ttk.Button(self.frame1, text='Start', command=self.startPlay)
		self.stopButton = ttk.Button(self.frame1, text='Stop & Exit', command=self.stopPlay)
		self.captureButton = ttk.Button(self.frame1, text='Capture', command=self.saveCapture)

		self.logArea = MyScrolledText(self.frame1, width=70)
		self.logArea.write = self.write
		sys.stdout = self.logArea

		self.frame1.grid(row=0,column=0,sticky='nwse')

		self.label1.grid(row=0,column=0,sticky='e')
		self.entry1.grid(row=0,column=1,sticky='w')
		self.reloadButton.grid(row=0,column=2)
		self.captureButton.grid(row=0,column=3)
		self.cb1.grid(row=0,column=5,sticky='e')
		
		self.logArea.grid(row=0,column=7,rowspan=3, sticky='nwse')
		
		self.label2.grid(row=1,column=0,sticky='e')
		self.entry2.grid(row=1,column=1,sticky='w')
		
		self.startButton.grid(row=1,column=5)
		self.stopButton.grid(row=1,column=6)
		
		self.preview.grid(row=2,column=0,columnspan=7, sticky='nw')

		for child in self.frame1.winfo_children():
			child.grid_configure(padx=5, pady=5)
		
		self.camera = CAMERA()
		self.openCamera()
		self.root.after(100, self.doProcess)
		self.commands = [Command.Sync('sync')]
	
	def openCamera(self):
		self.camera.openCamera(self.cameraID.get())
	
	def startPlay(self):
		# if self.autoPlayer is None:
		# 	self.autoPlayer = auto.AutoPlayer()
		# 	self.autoPlayer.cap.openCamera(self.cameraID.get())
		# 	self.autoPlayer.ser.openSerial("COM"+str(self.comPort.get()))
		# 	self.autoPlayer.start()
		# else:
		# 	self.autoPlayer.resume()
		print("Hello")
		
		self.startButton["text"] = "Pause"
		self.startButton["command"] = self.pausePlay
	
	def pausePlay(self):
		# self.autoPlayer.pause()
		
		self.startButton["text"] = "Start"
		self.startButton["command"] = self.startPlay
		
	def stopPlay(self):
		# self.autoPlayer.stop()
		exit()
	
	def saveCapture(self):
		self.camera.saveCapture()
	
	def doProcess(self):
		image_bgr = self.camera.readFrame()
		if self.showPreview.get() and image_bgr is not None:
			image_bgr = cv2.resize(image_bgr, (640, 360))
			image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB) 
			image_pil = Image.fromarray(image_rgb) 
			image_tk  = ImageTk.PhotoImage(image_pil)
			
			self.preview.im = image_tk
			self.preview['image']=image_tk
		
		self.root.after(100, self.doProcess)
	
	def write(self, str):
		self.logArea.insert(tk.END, str)
		time.sleep(0.0001)
		self.logArea.see(tk.END)

if __name__ == "__main__":
	gui = GUI()
	gui.root.mainloop()
