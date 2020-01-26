#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, os
from tkinter.scrolledtext import ScrolledText
import tkinter as tk
from tkinter import ttk
import cv2, json, time
import McuCommand, PythonCommand, UnitCommand
import Camera, Sender
from Keys import KeyPress
from Keyboard import SwitchKeyboardController
from Camera import Camera
from GuiAssets import CaptureArea, ControllerGUI

NAME = "Poke-Controller"
VERSION = "v1.0"
SETTING_PATH = "./settings.json"

# To avoid the error says 'ScrolledText' object has no attribute 'flush'
class MyScrolledText(ScrolledText):
	def flush(self):
		pass

# Main GUI
class GUI:
	def __init__(self):
		# NOTE: I'm gonna rewrite this function because this is not a good coding style

		self.root = tk.Tk()
		self.root.title(NAME + '  ' + VERSION)
		self.frame1 = ttk.Frame(
			self.root,
			height=720,
			width=1280,
			relief='flat',
			borderwidth=5)
		self.controller = None
		self.keyPress = None
		self.keyboard = None

		# label frames
		self.lf = ttk.Labelframe(self.frame1, text='Command', padding=5)
		self.serial_lf = ttk.Labelframe(self.frame1, text='Serial Settings', padding=5)
		self.camera_lf = ttk.Labelframe(self.frame1, text='Camera', padding=5)
		self.control_lf = ttk.Labelframe(self.frame1, text='Controller', padding=5)

		# frames
		self.camera_f1 = ttk.Frame(self.camera_lf, relief='flat')
		self.camera_f2 = ttk.Frame(self.camera_lf, relief='flat')
		self.serial_f1 = ttk.Frame(self.serial_lf, relief='flat')
		self.serial_f2 = ttk.Frame(self.serial_lf, relief='flat')

		# log area
		self.logArea = MyScrolledText(self.frame1, width=70)
		self.logArea.write = self.write
		sys.stdout = self.logArea

		# load settings file
		self.loadSettings()

		# camera settings
		self.label1 = ttk.Label(self.camera_f1, text='Camera ID:')
		self.cameraID = tk.IntVar()
		self.cameraID.set(int(self.settings['camera_id']))
		self.camera_entry = None
		if os.name == 'nt':
			try:
				self.locateCameraCmbbox()
			except:
				# Locate an entry instead whenever dll is not imported successfully
				self.camera_entry = ttk.Entry(self.camera_f1, width=5, textvariable=self.cameraID)
		else:
			self.camera_entry = ttk.Entry(self.camera_f1, width=5, textvariable=self.cameraID)

		# open up a camera
		self.camera = Camera()
		self.openCamera()

		self.showPreview = tk.BooleanVar()
		self.cb1 = ttk.Checkbutton(
			self.camera_f1,
			padding=5,
			text='Show Realtime',
			onvalue=True,
			offvalue=False,
			variable=self.showPreview)
		self.showPreview.set(True)

		self.label2 = ttk.Label(self.serial_f1, text='COM Port:')
		self.comPort = tk.IntVar()
		self.comPort.set(int(self.settings['com_port']))
		self.entry2 = ttk.Entry(self.serial_f1, width=5, textvariable=self.comPort)
		self.preview = CaptureArea(self.camera, self.settings['fps'], self.showPreview, self.camera_lf)

		# activate serial communication
		self.ser = Sender.Sender()
		self.activateSerial()

		self.v1 = tk.StringVar(value='Python')
		self.rb1 = ttk.Radiobutton(self.lf, text='Mcu', value='Mcu', variable=self.v1, command=self.setCommandCmbbox)
		self.rb2 = ttk.Radiobutton(self.lf, text='Python', value='Python', variable=self.v1, command=self.setCommandCmbbox)
		self.reloadCommandButton = ttk.Button(self.lf, text='Reload', command=self.reloadCommand)

		self.reloadButton = ttk.Button(self.camera_f1, text='Reload Cam', command=self.openCamera)
		self.reloadComPort = ttk.Button(self.serial_f1, text='Reload Port', command=self.activateSerial)
		self.startButton = ttk.Button(self.lf, text='Start', command=self.startPlay)
		self.captureButton = ttk.Button(self.camera_f1, text='Capture', command=self.preview.saveCapture)

		self.showSerial = tk.BooleanVar()
		self.showSerial.set(False)
		self.cb_show_ser = ttk.Checkbutton(
			self.serial_f2,
			padding=5,
			text='Show Serial',
			onvalue=True,
			offvalue=False,
			variable=self.showSerial,
			command=lambda: self.ser.setIsShowSerial(self.showSerial.get()))

		# simple controller
		self.useKeyboard = tk.BooleanVar()
		self.cb_use_keyboard = ttk.Checkbutton(
			self.control_lf, text='Use Keyboard',
			onvalue=True, offvalue=False, variable=self.useKeyboard,
			command=self.activateKeyboard)
		self.useKeyboard.set(False)
		self.simpleConButton = ttk.Button(self.control_lf, text='Controller', command=self.createControllerWindow)

		# fps
		self.label3 = ttk.Label(self.camera_f2, text='FPS:')
		self.fps = tk.StringVar()
		self.fps.set(str(self.settings['fps']))
		self.fps_cb = ttk.Combobox(self.camera_f2, textvariable=self.fps, width=2, state="readonly")
		self.fps_cb['values'] = [45, 30, 15]
		self.fps_cb.bind('<<ComboboxSelected>>', self.applyFps)
		self.fps_cb.current(self.fps_cb['values'].index(self.fps.get()))

		# commands
		self.mcu_name = tk.StringVar()
		self.mcu_cb = ttk.Combobox(self.lf, textvariable=self.mcu_name, state="readonly")
		self.mcu_cb.bind('<<ComboboxSelected>>', self.assignMcuCommand)
		self.py_name = tk.StringVar()
		self.py_cb = ttk.Combobox(self.lf, textvariable=self.py_name, state="readonly")
		self.py_cb.bind('<<ComboboxSelected>>', self.assignPythonCommand)
		self.setCommandItems()
		self.assignCommand()

		self.partition1 = ttk.Label(self.camera_f1, text=' / ')
		self.partition2 = ttk.Label(self.camera_f1, text=' / ')

		self.frame1.grid(row=0,column=0,sticky='nwse')
		self.logArea.grid(row=0,column=7,rowspan=5, sticky='nwse')

		# camera
		self.camera_lf.grid(row=0,column=0,columnspan=3, sticky='nw')
		self.camera_f1.grid(row=0,column=0, sticky='nw')
		self.camera_f2.grid(row=2,column=0, sticky='nw', pady=(5, 0))
		self.preview.grid(row=1,column=0,columnspan=7, sticky='nw')
		self.label1.pack(side=tk.LEFT)
		self.camera_entry.pack(side=tk.LEFT, padx=5)

		self.reloadButton.pack(side=tk.LEFT)
		self.partition1.pack(side=tk.LEFT, padx=10)
		self.cb1.pack(side=tk.LEFT)
		self.partition2.pack(side=tk.LEFT, padx=10)
		self.captureButton.pack(side=tk.LEFT)
		self.label3.pack(side=tk.LEFT)
		self.fps_cb.pack(side=tk.LEFT, padx=5)

		# serial
		self.serial_lf.grid(row=1,column=0, sticky='nw')
		self.serial_f1.grid(row=0,column=0, sticky='nw')
		self.serial_f2.grid(row=1,column=0, sticky='nw', pady=(5, 0))
		self.label2.pack(side=tk.LEFT)
		self.entry2.pack(side=tk.LEFT, padx=5)
		self.reloadComPort.pack(side=tk.LEFT)
		self.cb_show_ser.pack(side=tk.LEFT)

		# controller simulator
		self.control_lf.grid(row=1, column=1, sticky='ne')
		self.cb_use_keyboard.grid(row=0, column=0)
		self.simpleConButton.grid(row=1, column=0, pady=(5,0))

		# commands selection
		self.lf.grid(row=1,column=2, rowspan=3, sticky='ne')
		self.rb1.grid(row=0,column=0, sticky='w')
		self.rb2.grid(row=1,column=0, sticky='w')
		self.setCommandCmbbox()
		self.reloadCommandButton.grid(row=3,column=1, sticky='e', pady=(10, 0))
		self.startButton.grid(row=3,column=2, sticky='e', pady=(10, 0))

		for child in self.frame1.winfo_children():
			if not type(child) is ttk.Combobox:
				child.grid_configure(padx=5, pady=5)

		self.root.protocol("WM_DELETE_WINDOW", self.exit)
		self.preview.startCapture()

	def setCommandItems(self):
		self.mcu_cb['values'] = [name for name in McuCommand.commands.keys()]
		self.mcu_cb.current(0)
		self.py_cb['values'] = [name for name in PythonCommand.commands.keys()]
		self.py_cb.current(0)

	def openCamera(self):
		self.camera.openCamera(self.cameraID.get())
		self.settings['camera_id'] = self.cameraID.get()
	
	def assignCamera(self, event):
		if os.name == 'nt':
			self.cameraID.set(self.camera_dic[self.cameraName.get()])

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
		if self.cur_command is None:
			print('No commands have been assinged yet.')

		# set and init selected command
		self.assignCommand()

		print(self.startButton["text"] + ' ' + self.cur_command.getName())
		self.cur_command.start(self.ser, self.stopPlayPost)

		self.startButton["text"] = "Stop"
		self.startButton["command"] = self.stopPlay

	def assignCommand(self):
		if self.v1.get() == 'Mcu':
			name = self.mcu_name.get()
			self.cur_command = McuCommand.commands[name](name)
		elif self.v1.get() == 'Python':
			name = self.py_name.get() 
			cmd_class = PythonCommand.commands[name]

			if issubclass(cmd_class, PythonCommand.ImageProcPythonCommand):
				self.cur_command = cmd_class(name, self.camera)
			else:
				self.cur_command = cmd_class(name)

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

		self.camera.destroy()
		cv2.destroyAllWindows()
		self.root.destroy()

	def applyFps(self, event):
		print('changed FPS to: ' + self.fps.get() + ' [fps]')
		self.preview.setFps(self.fps.get())
		self.settings['fps'] = self.fps.get()

	def assignMcuCommand(self, event):
		print('changed to mcu command: ' + self.mcu_name.get())

	def assignPythonCommand(self, event):
		print('changed to python command: ' + self.py_name.get())

	def setCommandCmbbox(self):
		if self.v1.get() == 'Mcu':
			self.mcu_cb.grid(row=0,column=1, columnspan=2, padx=(10, 0))
			self.py_cb.grid_remove()
			self.assignMcuCommand(None)
		elif self.v1.get() == 'Python':
			self.mcu_cb.grid_remove()
			self.py_cb.grid(row=0,column=1, columnspan=2, padx=(10, 0))
			self.assignPythonCommand(None)

	def locateCameraCmbbox(self):
		import clr
		clr.AddReference(r"..\DirectShowLib\DirectShowLib-2005")
		from DirectShowLib import DsDevice, FilterCategory

		# Get names of detected camera devices
		captureDevices = DsDevice.GetDevicesOfCat(FilterCategory.VideoInputDevice)
		self.camera_dic = {device.Name: cam_id for cam_id, device in enumerate(captureDevices)}
		self.camera_dic['Disable'] = max(list(self.camera_dic.values())) + 1
		dev_num = len(self.camera_dic)

		if self.cameraID.get() > dev_num - 1:
			print('inappropriate camera ID! -> set to 0')
			self.cameraID.set(0)
			if dev_num == 0: print('No camera devices can be found.')

		# locate a combobox instead of an entry
		self.cameraName = tk.StringVar()
		self.label1['text'] = 'Camera: '
		self.camera_entry = ttk.Combobox(self.camera_f1, width=30, textvariable=self.cameraName, state="readonly")
		self.camera_entry['values'] = [device for device in self.camera_dic.keys()]
		self.camera_entry.bind('<<ComboboxSelected>>', self.assignCamera)
		if not dev_num == 0:
			self.camera_entry.current(self.cameraID.get())

	def activateSerial(self):
		if self.ser.isOpened():
			print('Port is already opened and being closed.')
			self.ser.closeSerial()
			self.keyPress = None
			self.activateSerial()
		else:
			if self.ser.openSerial(self.comPort.get()):
				self.settings['com_port'] = self.comPort.get()
				print('COM Port ' + str(self.comPort.get()) + ' connected successfully')
				self.keyPress = KeyPress(self.ser)

	def createControllerWindow(self):
		if not self.controller is None:
			self.controller.focus_force()
			return

		window = ControllerGUI(self.root, self.ser)
		window.protocol("WM_DELETE_WINDOW", self.closingController)
		self.controller = window
	
	def activateKeyboard(self):
		if self.useKeyboard.get() == True:
			# enable Keyboard as controller
			if self.keyboard is None:
				self.keyboard = SwitchKeyboardController(self.keyPress)
				self.keyboard.listen()
		
			# bind focus
			if os.name == 'nt':
				self.root.bind("<FocusIn>", self.onFocusInController)
				self.root.bind("<FocusOut>", self.onFocusOutController)

		elif self.useKeyboard.get() == False:
			if os.name == 'nt': # NOTE: Idk why but self.keyboard.stop() makes crash on Linux
				if not self.keyboard is None:
					# stop listening to keyboard events
					self.keyboard.stop()
					self.keyboard = None

					self.root.bind("<FocusIn>", lambda _: None)
					self.root.bind("<FocusOut>", lambda _: None)

	def closingController(self):
		self.controller.destroy()
		self.controller = None

	def onFocusInController(self, event):
		# enable Keyboard as controller
		if self.keyboard is None:
			self.keyboard = SwitchKeyboardController(self.keyPress)
			self.keyboard.listen()

	def onFocusOutController(self, event):
		# stop listening to keyboard events
		if not self.keyboard is None:
			self.keyboard.stop()
			self.keyboard = None

	def write(self, str):
		self.logArea.insert(tk.END, str)
		time.sleep(0.0001)
		self.logArea.see(tk.END)

	def reloadCommand(self):
		import importlib
		importlib.reload(McuCommand)
		importlib.reload(PythonCommand)
		importlib.reload(UnitCommand)

		if self.v1.get() == 'Mcu':
			visibledCb = self.mcu_cb
		elif self.v1.get() == 'Python':
			visibledCb = self.py_cb

		oldval = visibledCb.get()
		self.setCommandItems()
		if(oldval in visibledCb['values']):
			visibledCb.set(oldval)
		print('Reload command modules.')

if __name__ == "__main__":
	gui = GUI()
	gui.root.mainloop()
