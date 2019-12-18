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
import McuCommand
import PythonCommand
import UnitCommand
import Sender

DEFAULT_CAMERA_ID = 0
DEFAULT_COM_PORT = 3

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
		# NOTE: I'm gonna rewrite this function because this is not a good coding style

		self.root = tk.Tk()
		self.root.title('Pokemon Controller')
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

		self.reloadButton = ttk.Button(self.frame1, text='Reload Cam', command=self.openCamera)
		self.reloadComPort = ttk.Button(self.frame1, text='Reload Port', command=self.activateSerial)
		self.startButton = ttk.Button(self.frame1, text='Start', command=self.startPlay)
		self.stopButton = ttk.Button(self.frame1, text='Exit', command=self.exit)
		self.captureButton = ttk.Button(self.frame1, text='Capture', command=self.saveCapture)

		# simple controller
		self.simpleConButton = ttk.Button(self.frame1, text='Controller', command=self.createControllerWindow)

		self.logArea = MyScrolledText(self.frame1, width=70)
		self.logArea.write = self.write
		sys.stdout = self.logArea

		# activate serial communication
		self.ser = Sender.Sender()
		self.activateSerial()

		# command radio button
		self.lf = ttk.Labelframe(self.frame1, text='Command Option', padding=5)

		self.v1 = tk.StringVar(value='Python')
		self.rb1 = ttk.Radiobutton(self.lf, text='Mcu', value='Mcu', variable=self.v1, command=self.selectCommandCmbbox)
		self.rb2 = ttk.Radiobutton(self.lf, text='Python', value='Python', variable=self.v1, command=self.selectCommandCmbbox)			

		# commands registration
		self.mcu_commands = [
			McuCommand.Mash_A('A連打'), 
			McuCommand.InfinityWatt('無限ワット'),
			McuCommand.InfinityId('無限IDくじ'),
		]
		self.py_commands = [
			PythonCommand.InfinityWatt('無限ワット'),
			PythonCommand.HoldTest('Hold Test')
		]
		self.hid_commands = [ # not visible
			PythonCommand.Sync('同期'),
			PythonCommand.Unsync('同期解除'),
		]
		self.cur_command = self.py_commands[0] # attach a top of python commands first

		self.mcu_cb = ttk.Combobox(self.frame1)
		self.mcu_cb['values'] = [c.getName() for c in self.mcu_commands]
		self.mcu_cb.bind('<<ComboboxSelected>>', self.assignMcuCommand)
		self.mcu_cb.current(0)
		self.mcu_cb['state'] = 'disabled'

		self.py_cb = ttk.Combobox(self.frame1)
		self.py_cb['values'] = [c.getName() for c in self.py_commands]
		self.py_cb.bind('<<ComboboxSelected>>', self.assignPythonCommand)
		self.py_cb.current(0)

		self.sync_btn = ttk.Button(self.frame1, text='Sync', command=lambda: self.hid_commands[0].start(self.ser))
		self.unsync_btn = ttk.Button(self.frame1, text='Unsync', command=lambda: self.hid_commands[1].start(self.ser))

		self.frame1.grid(row=0,column=0,sticky='nwse')
		
		self.preview.grid(row=0,column=0,columnspan=7, sticky='nw')
		self.logArea.grid(row=0,column=7,rowspan=3, sticky='nwse')

		# camera & com port
		self.label1.grid(row=1,column=0, sticky='w')
		self.entry1.grid(row=1,column=1, sticky='w')
		self.reloadButton.grid(row=1,column=2, sticky='w')
		self.label2.grid(row=2,column=0, sticky='w')
		self.entry2.grid(row=2,column=1, sticky='w')
		self.reloadComPort.grid(row=2,column=2, sticky='w')

		self.cb1.grid(row=1,column=3, sticky='w')
		self.captureButton.grid(row=2,column=3)

		# commands selection
		self.lf.grid(row=3,column=5, rowspan=2)
		self.rb1.grid(row=2,column=5, sticky='nwse')
		self.rb2.grid(row=3,column=5, sticky='nwse')
		self.mcu_cb.grid(row=3, column=6)
		self.py_cb.grid(row=4, column=6)
		self.sync_btn.grid(row=4, column=3)
		self.unsync_btn.grid(row=4, column=4)

		self.stopButton.grid(row=1,column=6)
		self.startButton.grid(row=2,column=6)
		self.simpleConButton.grid(row=4, column=2)

		for child in self.frame1.winfo_children():
			child.grid_configure(padx=5, pady=5)

		self.camera = CAMERA()
		self.openCamera()
		self.root.after(100, self.doProcess)

	def openCamera(self):
		self.camera.openCamera(self.cameraID.get())
	
	def startPlay(self):
		print(self.startButton["text"] + ' ' + self.cur_command.getName())
		self.cur_command.start(self.ser)
		
		self.startButton["text"] = "Stop"
		self.startButton["command"] = self.stopPlay
	
	def stopPlay(self):
		print(self.startButton["text"] + ' ' + self.cur_command.getName())
		self.startButton["state"] = "disabled"
		self.cur_command.end(self.ser, self.stopPlayPost)
	
	def stopPlayPost(self):
		self.startButton["text"] = "Start"
		self.startButton["command"] = self.startPlay
		self.startButton["state"] = "normal"
		
	def exit(self):
		self.ser.closeSerial()
		print("serial disconnected")
		self.root.destroy()
	
	def saveCapture(self):
		self.camera.saveCapture()

	def assignMcuCommand(self, event):
		self.cur_command = self.mcu_commands[self.mcu_cb.current()]
		print('changed to mcu command: ' + self.cur_command.getName())
	
	def assignPythonCommand(self, event):
		self.cur_command = self.py_commands[self.py_cb.current()]
		print('changed to python command: ' + self.cur_command.getName())

	def selectCommandCmbbox(self):
		if self.v1.get() == 'Mcu':
			self.mcu_cb['state'] = 'normal'
			self.py_cb['state'] = 'disabled'
			self.assignMcuCommand(None)
		elif self.v1.get() == 'Python':
			self.mcu_cb['state'] = 'disabled'
			self.py_cb['state'] = 'normal'
			self.assignPythonCommand(None)
	
	def activateSerial(self):
		try:
			self.ser.openSerial("COM"+str(self.comPort.get()))
		except:
			print('COM Port: can\'t be established')

	def createControllerWindow(self):
		window = tk.Toplevel(self.root)
		window.title('Simple Switch Controller')
		window.geometry("%dx%d%+d%+d" % (800, 200, 250, 125))

		ttk.Button(window, text='A', command=lambda: UnitCommand.A().start(self.ser)).grid(row=5, column=11)
		ttk.Button(window, text='B', command=lambda: UnitCommand.B().start(self.ser)).grid(row=6, column=10)
		ttk.Button(window, text='X', command=lambda: UnitCommand.X().start(self.ser)).grid(row=4, column=10)
		ttk.Button(window, text='Y', command=lambda: UnitCommand.Y().start(self.ser)).grid(row=5, column=9)
		ttk.Button(window, text='L', command=lambda: UnitCommand.L().start(self.ser)).grid(row=1, column=1)
		ttk.Button(window, text='R', command=lambda: UnitCommand.R().start(self.ser)).grid(row=1, column=10)
		ttk.Button(window, text='ZL', command=lambda: UnitCommand.ZL().start(self.ser)).grid(row=0, column=1)
		ttk.Button(window, text='ZR', command=lambda: UnitCommand.ZR().start(self.ser)).grid(row=0, column=10)
		ttk.Button(window, text='MINUS', command=lambda: UnitCommand.MINUS().start(self.ser)).grid(row=3, column=3)
		ttk.Button(window, text='PLUS', command=lambda: UnitCommand.PLUS().start(self.ser)).grid(row=3, column=7)
		ttk.Button(window, text='LCLICK', command=lambda: UnitCommand.LCLICK().start(self.ser)).grid(row=4, column=1)
		ttk.Button(window, text='RCLICK', command=lambda: UnitCommand.RCLICK().start(self.ser)).grid(row=8, column=10)
		ttk.Button(window, text='HOME', command=lambda: UnitCommand.HOME().start(self.ser)).grid(row=4, column=6)
		ttk.Button(window, text='CAP', command=lambda: UnitCommand.CAPTURE().start(self.ser)).grid(row=4, column=4)
		ttk.Button(window, text='UP', command=lambda: UnitCommand.UP().start(self.ser)).grid(row=6, column=1)
		ttk.Button(window, text='RIGHT', command=lambda: UnitCommand.RIGHT().start(self.ser)).grid(row=7, column=2)
		ttk.Button(window, text='DOWN', command=lambda: UnitCommand.DOWN().start(self.ser)).grid(row=8, column=1)
		ttk.Button(window, text='LEFT', command=lambda: UnitCommand.LEFT().start(self.ser)).grid(row=7, column=0)

		for child in window.winfo_children():
			child['width'] = 8

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
