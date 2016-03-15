"""This is a 2 player arcade shooting game where both players 
control a rocket and try to shoot eachother with rockets."""

#!/usr/bin/env python3
import pygame
import random
import cProfile
from Vector2D import *


SCREEN_X = 1920
SCREEN_Y = 1080
SCREEN = (SCREEN_X, SCREEN_Y)



BACKGROUND_FNAME = "sprites/arcadebackground.jpg"
background = pygame.image.load(BACKGROUND_FNAME)
background = pygame.transform.scale(background, (SCREEN_X, SCREEN_Y))

RED = (204,0,0)
BLUE = (0,50,255)
YELLOW = (230,230,30)
WHITE = (255,255,255)
BLACK = (0,0,0)

FPS = 60

class Engine:
	"""This is the engine class"""
	def __init__(self):
		self.rockets = []
		self.rocketshot = []


	def eventhandler(self):
		"""The eventhandler"""
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit()
			
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_q:
					exit()
	def logic(self):
		self.eventhandler()

	def wallcollide(self):
		pass
		
class Movingobject:
	def __init__(self):
		self.gravity = 5

	def rotate(self):
		pass

class Rocket(Movingobject): 
	"""The class for rocket, broombroom"""
	def __initi__(self):
		super().__init__(self)


def main():
	pygame.init()
	pygame.display.set_caption("Mayhem")
	screen = pygame.display.set_mode((SCREEN),pygame.FULLSCREEN)	#FULLSCREEN
	#screen = pygame.display.set_mode((SCREEN), 0, 32 )				#WINDOWED

	clock = pygame.time.Clock()
	time = clock.tick(FPS)
	engine = Engine()

	while True:
		engine.logic()
		screen.blit(background, (0,0))
		pygame.display.update()

if __name__ == "__main__":
	main()