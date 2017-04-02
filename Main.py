#-*- encoding: utf-8 -*-
import sys, string, os
import pygame
import time
from pygame.locals import *
from GameBoard import *
from TitleMenu import *
import os

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (100,100)
pygame.init()
window = pygame.display.set_mode((460, 590)) 
pygame.display.set_caption('Coway Game of Life')
board = GameBoard()
title = TitleController(window)
title.main(board)
window = board.createWindow()
#chessbord.draw(window)
#window.blit(curPos, (left, top))
bInit = 1
fps = 30
clock = pygame.time.Clock()
while True:
	clock.tick(fps)
	board.draw(window)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				sys.exit()
			keyname = pygame.key.get_pressed()
	pygame.display.update()

