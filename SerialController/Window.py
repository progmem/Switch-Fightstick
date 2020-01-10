#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, os
from tkinter.scrolledtext import ScrolledText
import tkinter as tk
from tkinter import ttk
import cv2
import json
from PIL import Image, ImageTk
import time
import datetime
import McuCommand
import PythonCommand
import UnitCommand
import Sender
from Keys import KeyPress
from Keyboard import SwitchKeyboardController

SETTING_PATH = "./settings.json"

# To avoid the error says 'ScrolledText' object has no attribute 'flush'
class MyScrolledText(ScrolledText):
	def flush(self):
		pass

class Camera:
	def __init__(self):
		self.camera = None
		self.capture_size = (1280, 720)
		
	def openCamera(self, cameraId):
		if self.camera is not None and self.camera.isOpened():
			self.camera.release()
			self.camera = None
		self.camera = cv2.VideoCapture(cameraId)
		if not self.camera.isOpened():
			print("Camera ID: " + str(cameraId) + " can't open.")
			return
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
		self.controller = None
		self.keyPress = None
		self.keyboard = None

		# log area
		self.logArea = MyScrolledText(self.frame1, width=70)
		self.logArea.write = self.write
		sys.stdout = self.logArea

		# load settings file
		self.loadSettings()
			
		self.label1 = ttk.Label(self.frame1, text='Camera ID:')
		self.cameraID = tk.IntVar()
		self.cameraID.set(int(self.settings['camera_id']))
		self.entry1 = ttk.Entry(self.frame1, width=5, textvariable=self.cameraID)

		# open up a camera
		self.camera = Camera()
		self.openCamera()

		self.showPreview = tk.BooleanVar()
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
		self.comPort.set(int(self.settings['com_port']))
		self.entry2 = ttk.Entry(self.frame1, width=5, textvariable=self.comPort)
		self.preview = ttk.Label(self.frame1) 

		# activate serial communication
		self.ser = Sender.Sender()
		self.activateSerial()

		self.reloadButton = ttk.Button(self.frame1, text='Reload Cam', command=self.openCamera)
		self.reloadComPort = ttk.Button(self.frame1, text='Reload Port', command=self.activateSerial)
		self.startButton = ttk.Button(self.frame1, text='Start', command=self.startPlay)
		self.captureButton = ttk.Button(self.frame1, text='Capture', command=self.saveCapture)

		self.showSerial = tk.BooleanVar()
		self.showSerial.set(False)
		self.cb_show_ser = ttk.Checkbutton(
			self.frame1,
			padding=5,
			text='Show Serial',
			onvalue=True,
			offvalue=False,
			variable=self.showSerial,
			command=lambda: self.ser.setIsShowSerial(self.showSerial.get()))

		# simple controller
		self.simpleConButton = ttk.Button(self.frame1, text='Controller', command=self.createControllerWindow)

		# fps
		self.label3 = ttk.Label(self.frame1, text='FPS:')
		self.fps = tk.StringVar()
		self.fps.set(str(self.settings['fps']))
		self.fps_cb = ttk.Combobox(self.frame1, textvariable=self.fps, width=2)
		self.fps_cb['values'] = [45, 30, 15]
		self.fps_cb.bind('<<ComboboxSelected>>', self.applyFps)
		self.fps_cb.current(self.fps_cb['values'].index(self.fps.get()))

		# command radio button
		self.lf = ttk.Labelframe(self.frame1, text='Command Option', padding=5)

		self.v1 = tk.StringVar(value='Python')
		self.rb1 = ttk.Radiobutton(self.lf, text='Mcu', value='Mcu', variable=self.v1, command=self.selectCommandCmbbox)
		self.rb2 = ttk.Radiobutton(self.lf, text='Python', value='Python', variable=self.v1, command=self.selectCommandCmbbox)			

		# commands registration
		self.mcu_commands = [
			McuCommand.Mash_A('A連打'), 
			McuCommand.AutoLeague('自動リーグ周回'),
			McuCommand.InfinityWatt('無限ワット'),
			McuCommand.InfinityId('無限IDくじ'),
		]
		self.py_commands = [
			PythonCommand.AutoHatching('自動孵化(画像認識)', self.camera),
			PythonCommand.CountHatching('固定数孵化(画像認識)', self.camera),
			PythonCommand.Debug('Debug', self.camera),
			PythonCommand.AutoRelease('自動リリース', self.camera),
			PythonCommand.Mash_A('A連打'),
			PythonCommand.AutoLeague('自動リーグ周回'),
			PythonCommand.InfinityWatt('無限ワット', False),
			PythonCommand.InfinityWatt('無限ワット(ランクマ)', True),
			PythonCommand.InfinityLottery('無限IDくじ(ランクマ)'),
			PythonCommand.InfinityBerry('無限きのみ(ランクマ)'),
			PythonCommand.InfinityCafe('無限カフェ(ランクマ)'),
			PythonCommand.InfinityBerryIP('無限きのみ(ランクマ/画像認識)', self.camera),
		]
		self.hid_commands = [ # not visible
			PythonCommand.Sync('同期'),
			PythonCommand.Unsync('同期解除'),
		]
		self.unit_dir_commands = [
			UnitCommand.UP(),
			UnitCommand.RIGHT(),
			UnitCommand.DOWN(),
			UnitCommand.LEFT(),
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
		self.logArea.grid(row=0,column=7,rowspan=5, sticky='nwse')

		# camera & com port & FPS
		self.label1.grid(row=1,column=0, sticky='w')
		self.entry1.grid(row=1,column=1, sticky='w')
		self.reloadButton.grid(row=1,column=2, sticky='w')
		self.label2.grid(row=2,column=0, sticky='w')
		self.entry2.grid(row=2,column=1, sticky='w')
		self.reloadComPort.grid(row=2,column=2, sticky='w')
		self.label3.grid(row=3,column=0, sticky='w')
		self.fps_cb.grid(row=3,column=1, sticky='w')

		self.cb1.grid(row=1,column=3, sticky='w')
		self.captureButton.grid(row=2,column=3)

		# commands selection
		self.lf.grid(row=3,column=5, rowspan=2)
		self.rb1.grid(row=2,column=5, sticky='nwse')
		self.rb2.grid(row=3,column=5, sticky='nwse')
		self.mcu_cb.grid(row=3, column=6)
		self.py_cb.grid(row=4, column=6)
		self.sync_btn.grid(row=1, column=5)
		self.unsync_btn.grid(row=2, column=5)

		self.startButton.grid(row=2,column=6)
		self.simpleConButton.grid(row=4, column=4)

		self.cb_show_ser.grid(row=4, column=3)

		for child in self.frame1.winfo_children():
			child.grid_configure(padx=5, pady=5)

		self.root.iconbitmap('../infinite.ico')
		self.root.protocol("WM_DELETE_WINDOW", self.exit)
		self.root.after(100, self.doProcess)

	def openCamera(self):
		self.camera.openCamera(self.cameraID.get())
		self.settings['camera_id'] = self.cameraID.get()
	
	def loadSettings(self):
		self.settings = None
		if os.path.isfile(SETTING_PATH):
			self.settings = json.load(open(SETTING_PATH, 'r'))
		else:
			default = {
				"camera_id": 0,
				"com_port": 1,
				"fps": "45"
			}
			json.dump(default, open(SETTING_PATH, 'w'), indent=4)
			print('default settings file has been created')
			self.loadSettings()
	
	def startPlay(self):
		print(self.startButton["text"] + ' ' + self.cur_command.getName())
		self.cur_command.start(self.ser, self.stopPlayPost)
		
		self.startButton["text"] = "Stop"
		self.startButton["command"] = self.stopPlay
	
	def stopPlay(self):
		print(self.startButton["text"] + ' ' + self.cur_command.getName())
		self.startButton["state"] = "disabled"
		self.cur_command.end(self.ser)
	
	def stopPlayPost(self):
		self.startButton["text"] = "Start"
		self.startButton["command"] = self.startPlay
		self.startButton["state"] = "normal"
		
	def exit(self):
		if self.ser.isOpened():
			self.ser.closeSerial()
			print("serial disconnected")
		
		# stop listening to keyboard events
		if not self.keyboard is None:
			self.keyboard.stop()
			self.keyboard = None

		# save settings
		json.dump(self.settings, open(SETTING_PATH, 'w'), indent=4)

		self.root.destroy()
	
	def saveCapture(self):
		self.camera.saveCapture()
	
	def applyFps(self, event):
		print('changed FPS to: ' + self.fps.get() + ' [fps]')
		self.settings['fps'] = self.fps.get()

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
			if self.ser.isOpened():
				print('Port is already opened and being closed.')
				self.ser.closeSerial()
				self.keyPress = None
				self.activateSerial()
			else:
				self.ser.openSerial("COM"+str(self.comPort.get()))
				self.settings['com_port'] = self.comPort.get()
				print('COM Port ' + str(self.comPort.get()) + ' connected successfully')
				self.keyPress = KeyPress(self.ser)
		except IOError:
			print('COM Port: can\'t be established')

	def createControllerWindow(self):
		if not self.controller is None:
			self.controller.focus_force()
			return

		window = tk.Toplevel(self.root)
		window.title('Simple Switch Controller')
		window.geometry("%dx%d%+d%+d" % (600, 300, 250, 125))

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
		ttk.Button(window, text='UP', command=lambda: self.unit_dir_commands[0].start(self.ser)).grid(row=6, column=1)
		ttk.Button(window, text='RIGHT', command=lambda: self.unit_dir_commands[1].start(self.ser)).grid(row=7, column=2)
		ttk.Button(window, text='DOWN', command=lambda: self.unit_dir_commands[2].start(self.ser)).grid(row=8, column=1)
		ttk.Button(window, text='LEFT', command=lambda: self.unit_dir_commands[3].start(self.ser)).grid(row=7, column=0)

		for child in window.winfo_children():
			child['width'] = 8

		ttk.Label(window, text='NOTE:').grid(row=9, column=0, columnspan=8, sticky='w', padx=10, pady=(20, 0))
		ttk.Label(window, text='Direction buttons are toggle switch.').grid(row=10, column=0, columnspan=8, sticky='w', padx=10, pady=3)
		ttk.Label(window, text='Key Arrangements are based on Switch Pro. Controller.').grid(row=11, column=0, columnspan=8, sticky='w', padx=10, pady=3)
		
		# enable Keyboard as controller
		self.keyboard = SwitchKeyboardController(self.keyPress)
		self.keyboard.listen()

		window.protocol("WM_DELETE_WINDOW", self.closingController)
		self.controller = window
	
	def closingController(self):
		# stop listening to keyboard events
		if not self.keyboard is None:
			self.keyboard.stop()
			self.keyboard = None

		self.controller.destroy()
		self.controller = None

	def doProcess(self):
		image_bgr = self.camera.readFrame()
		if self.showPreview.get() and image_bgr is not None:
			image_bgr = cv2.resize(image_bgr, (640, 360))
			image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB) 
			image_pil = Image.fromarray(image_rgb) 
			image_tk  = ImageTk.PhotoImage(image_pil)
			
			self.preview.im = image_tk
			self.preview['image']=image_tk

		self.root.after((int)(16 * (60 / int(self.fps.get()))), self.doProcess)
	
	def write(self, str):
		self.logArea.insert(tk.END, str)
		time.sleep(0.0001)
		self.logArea.see(tk.END)

if __name__ == "__main__":
	gui = GUI()
	gui.root.mainloop()
