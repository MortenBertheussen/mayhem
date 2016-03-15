"""This is a 2 player arcade shooting game where both players 
control a rocket and try to shoot eachother with rockets."""

#!/usr/bin/env python3
import pygame
import random
import cProfile
from gameconstants import *
from Vector2D import *
from Movingobjects import *


BACKGROUND_FNAME = "sprites/arcadebackground.jpg"
background = pygame.image.load(BACKGROUND_FNAME)
background = pygame.transform.scale(background, (SCREEN_X, SCREEN_Y))

class Engine:
	"""This is the engine class"""
	def __init__(self):
		self.rocket = Rocket()
		self.rocketshot = []
		self.otherrockets = []

	def eventhandler(self):
		"""The eventhandler"""
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit()
			
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_q:
					exit()
				if event.key == pygame.K_SPACE:
					self.rocket.engineOn = True
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_SPACE:
					self.rocket.engineOn = False

	def logic(self, screen):
		self.eventhandler()
		self.rocket.logic(screen)

def main():
	pygame.init()
	pygame.display.set_caption("Mayhem")
	#screen = pygame.display.set_mode((SCREEN),pygame.FULLSCREEN)	#FULLSCREEN
	screen = pygame.display.set_mode((SCREEN), 0, 32 )				#WINDOWED
	clock = pygame.time.Clock()
	engine = Engine() #Initialize game engine

	while True:
		time = clock.tick(FPS)

		screen.blit(background, (0,0))
		engine.logic(screen)
		pygame.display.update()

if __name__ == "__main__":
	main()