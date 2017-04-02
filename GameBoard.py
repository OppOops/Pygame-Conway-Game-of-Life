#-*- encoding: utf-8 -*-
from TitleMenu import *
import sys, string, os
import pygame, time
import random


class CellularAutomaton:
	def __init__(self):
		self.dic = {-8:0, -7:0, -6:0, -5:0, -4:0, -3:1,
					-2:0, -1:0, 0:0, 1:0, 2:1, 3:1, 4:0,
					5:0, 6:0, 7:0, 8:0}
		
	def updateBoarderCount(self, board, m, n, i, k):
		countN = 0
		for s in xrange(i-1, i+2):
			for t in xrange(k-1,k+2):
				if (s<m) and (t<n) and (s!=i or t!=k) and board[s][t] > 0:
					countN += 1
				elif ((s >= m) or (t>=n)) and board[s%m][t%n] > 0:
					countN += 1
		if board[i][k] == 0:
			board[i][k] = -countN
		else:
			board[i][k] = max(board[i][k], countN)
		
	def updateCount(self, board, m, n):
		for i in xrange(1,m-1):
			for k in xrange(1,n-1):
				countN = 0
				for s in xrange(i-1, i+2):
					for t in xrange(k-1,k+2):
						if (s!=i or t!=k) and board[s][t] > 0:
							countN += 1
				if board[i][k] == 0:
					board[i][k] = -countN
				else:
					board[i][k] = max(board[i][k], countN)
		for i in xrange(m):
			self.updateBoarderCount(board, m, n, i, 0)
			if n!=1:
				self.updateBoarderCount(board, m, n, i, n-1)
		for k in xrange(1,n-1):
			self.updateBoarderCount(board, m, n, 0, k)
			if m!=1:
				self.updateBoarderCount(board, m, n, m-1, k)
	
	def assignGen(self, board, m, n):
		mapDict = self.dic
		count = 0
		for i in xrange(m):
			for k in xrange(n):
				val = mapDict[board[i][k]]
				board[i][k] = val
				if val == 1:
					count += 1
		return count
		
	def nextGen(self, board):
		m = len(board)
		n = len(board[0])
		self.updateCount(board,m,n)
		return self.assignGen(board,m,n)
		
class GameModel:
	def __init__(self):
		self.m = 30
		self.n = 30
		self.update = 100
		self.sample = 200
		self.csize  = 10
		self.iter   = 0
		self.lives  = 0
		self.cellatm = CellularAutomaton()
	
	def next(self):
		self.iter += 1
		self.lives = self.cellatm.nextGen(self.map)
	
	def genRandom(self, m, n, s):
		random.seed()
		arr    = range(m*n)
		for i in xrange(len(arr)-1,0,-1):
			pos = random.randint(0, i)
			arr[pos], arr[i] = arr[i], arr[pos]
		return arr[:s]
	
	def parseInput(self, result):
		try:
			m = int(result['m'])
			n = int(result['n'])
			csize = int(result['cellSize'])
			if m<=0 or n<=0:
				return False
			if csize<=0 or csize >= m or csize >= n:
				return False
			elif int(result['Updatetime'])<100:
				return False
			elif int(result['initCells'])> m*n:
				return False
			else:
				return True
		except:
			return False
	
	def setConfig(self, result):
		if self.parseInput(result) == False:
			return False
		self.m = int(result['m'])
		self.n = int(result['n'])
		self.update = int(result['Updatetime'])
		self.sample = int(result['initCells'])
		self.csize = int(result['cellSize'])
		self.createMap()
		return True
	
	def createMap(self):
		self.map   = [None] * self.m
		for i in xrange(self.m):
			self.map[i] = [0] * self.n
		for loc in self.genRandom(self.m, self.n, self.sample):
			y = loc % self.n
			x = (loc - y) // self.n
			try:
				self.map[x][y] = 1
			except:
				print x,y, self.m, self.n
		
class GameBoard:
	def __init__(self):
		self.tipInfo = ""
		self.model   = GameModel()
		self.s = None
		self.e = None
	
	def clock(self):
		if self.s == None:
			self.s = time.time()
			return False
		self.e = time.time()
		if (self.e - self.s)*1000 >= self.model.update:
			self.s = self.e
			return True
		else:
			return False
	
	def load_font(self, txt):
		font = pygame.font.SysFont('Arial', 20)
		text = font.render(txt, 1, (255, 0, 0))
		textpos = text.get_rect()
		return text, textpos
	
	def createWindow(self):
		x = self.model.m * self.model.csize
		y = self.model.n * self.model.csize
		window = pygame.display.set_mode((x, y))
		return window
	
	def drawModel(self, window):
		map = self.model.map
		sz  = self.model.csize
		for i in xrange(len(map)):
			for k in xrange(len(map[i])):
				if map[i][k] == 1:
					pygame.draw.rect(window, (255,255,255), (i*sz,k*sz,sz,sz), 0)
	
	def __redrawBorad(self, window): #TODO
		window.fill((0,0,0))
		#font = pygame.font.SysFont('Arial', 24)
		self.window = window
		if self.clock():
			self.model.next()
		self.drawModel(window)

	def __showTipInfo(self, window):
		y = self.model.n * self.model.csize
		text, textpos = self.load_font("cells: " + str(self.model.lives))
		textpos = Rect(0, y-45, 40, 28)
		window.blit(text, textpos)
		text, textpos = self.load_font("generation: " + str(self.model.iter))
		textpos = Rect(0, y-30, 40, 28)
		window.blit(text, textpos)
	
	def draw(self, window):
		self.__redrawBorad(window)
		self.__showTipInfo(window)
		
	def setTip(self, tipText):
		self.tipInfo = tipText
	
	def setConfig(self, result):
		return self.model.setConfig(result)
