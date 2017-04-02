#-*- encoding: utf-8 -*-
import sys, time
import datetime  # for datetime
import operator
import pygame
import Tkinter
from GameBoard import *
from pygame.locals import *
from threading import Thread
from Queue import Queue
import pygubu
import random

class OptionController:
	def __init__(self, stage):
		self.stage = stage
		self.result = None
		self.cancelFlag = False
	
	def main(self):
		self.createDialog()
		return self.result
	
	def ok(self):
		result = self.dig.getVars(('m', 'n', 'Updatetime','initCells','cellSize'))
		if self.stage.setConfig(result) == False:
			result = None
		self.result = result
		self.dig.close()
		
	def cancel(self):
		self.result = False
		self.dig.close()
		
	def createDialog(self):
		uiFile  = 'config_single.ui'
		binding = {'cancel_event': self.cancel, 'ok_event': self.ok}
		self.dig = Dialog(uiFile, binding)
		self.dig.protocol("WM_DELETE_WINDOW", self.cancel)
		self.dig.show()

	
class DialogHookController(Thread):
	def __init__(self, dialog, message, endAll, remote):	
		Thread.__init__(self)
		self.dialog = dialog
		self.message = message
		self.endAll  = endAll
		self.remote = remote
		
	def checkRStop(self):
		if self.remote.empty() == False:
			return True
		else:
			return False
			
	def __close(self, msg):
		self.dialog.quit()
		self.endAll.put(msg)
					
	def stop(self):
		self.message.put(False)
		
	def hook(self):
		try:
			if(self.message.empty())==False:
				return False
			if(pygame.display.get_active())==True and self.dialog.focus_get()==None:
				self.dialog.focus_force()
			return True
		except:
			return False

	def run(self):
		clock = pygame.time.Clock()
		while self.hook():
			clock.tick()
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.__close('end')
					return
			if(self.checkRStop()):
				self.__close('remote')
				return
		trash = self.message.get()
		
class DialogController:
	def __init__(self, guiApp):
		self.message = Queue()
		self.endAll  = Queue()
		self.remote = Queue()
		self.thread = DialogHookController(guiApp, self.message, self.endAll, self.remote)
		self.dialog = guiApp
		self.stopFlag = False
	
	def close(self):
		self.thread.stop()
		self.stopFlag = True
		self.dialog.destroy()
	
	def run(self):
		self.thread.start()
		self.dialog.mainloop()
		if not self.endAll.empty():
			msg = self.endAll.get()
			if(msg == 'end'):
				sys.exit()
			else:
				self.dialog.destroy()
				return
		elif not(self.stopFlag):
			self.thread.stop()
			
class Dialog(Tkinter.Tk):
	__path = 'UI/'
	
	def __init__(self, UIfile, binding, title="Settings"):
		Tkinter.Tk.__init__(self)
		self.title(title)
		self.resizable(width=Tkinter.FALSE, height=Tkinter.FALSE)
		builder = pygubu.Builder()
		builder.add_from_file(self.__path + UIfile)
		mainwindow = builder.get_object('Frame', self)
		builder.connect_callbacks(binding)
		self.builder = builder
		self.dc = DialogController(self)
	
	def show(self):
		self.dc.run()
	
	def getRemoteQueue(self):
		return self.dc.remote
	
	def getVars(self, names):
		result = dict()
		for n in names:
			result[n] = self.getVar(n)
		return result
	
	def getVar(self, name):
		try:
			return self.builder.get_variable(name).get()
		except:
			return None
	
	def setVar(self, name, value):
		try:
			var = self.builder.get_variable(name)
			var.set(value)
			return True
		except Exception:
			return False
	
	def close(self):
		self.dc.close()
		
class MessageBox:	
	def __init__(self, message, title):
		self.dig = Dialog('message_box.ui', {'ok_event':self.ok }, title)
		self.dig.setVar('error_msg', message)
		
	def show(self):
		self.dig.show()
	
	def ok(self):
		self.dig.close()
		
class TitleController:
	def __init__(self, window):
		self.win = window
	
	def redraw(self):
		self.win.fill((0,0,0))
			
	def openDia(self, controller):
		window = OptionController(controller)
		result = window.main() 
		if result == False:
			sys.exit()
		return result
	
	def main(self, controller):
		self.redraw()
		while self.openDia(controller) == None:
			continue
	