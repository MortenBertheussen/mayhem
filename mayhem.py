"""This is a 2 player arcade shooting game where both players 
control a rocket and try to shoot eachother with rockets."""

#!/usr/bin/env python3
import pygame
import random
import math
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
		self.sprites = pygame.sprite.Group()
		self.sprites.add(self.rocket)

	def eventhandler(self):
		"""The eventhandler"""
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit()
			
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_q:
					exit()
				if event.key == pygame.K_UP:
					self.rocket.engineOn = True
				if event.key == pygame.K_LEFT:
					self.rocket.turnLeft = True
				if event.key == pygame.K_RIGHT:
					self.rocket.turnRight = True
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_UP:
					self.rocket.engineOn = False
				if event.key == pygame.K_LEFT:
					self.rocket.turnLeft = False
				if event.key == pygame.K_RIGHT:
					self.rocket.turnRight = False

	def logic(self, screen):
		self.sprites.update()
		self.eventhandler()
		self.rocket.logic(screen)
		self.sprites.draw(screen)
		pygame.display.update()

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

if __name__ == "__main__":
	main()