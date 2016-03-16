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
		self.rocket2 = Rocket()
		self.otherrockets = []
		self.obstacle = []
		self.obstacle_sprites = pygame.sprite.Group()
		self.bullet_sprites = pygame.sprite.Group()
		self.sprites = pygame.sprite.Group()
		self.sprites.add(self.rocket)
		self.sprites.add(self.rocket2)

	def eventhandler(self):
		"""The eventhandler"""
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit()
			
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_q:
					exit()
				#Player 1
				if event.key == pygame.K_UP:
					self.rocket.engineOn = True
				if event.key == pygame.K_LEFT:
					self.rocket.turnLeft = True
				if event.key == pygame.K_RIGHT:
					self.rocket.turnRight = True
				if event.key == pygame.K_KP_ENTER:
					bullet = self.rocket.shoot()
					self.bullet_sprites.add(bullet)
					self.sprites.add(bullet)

				#Player 2
				if event.key == pygame.K_w:
					self.rocket2.engineOn = True
				if event.key == pygame.K_a:
					self.rocket2.turnLeft = True
				if event.key == pygame.K_d:
					self.rocket2.turnRight = True
				if event.key == pygame.K_SPACE:
					bullet = self.rocket2.shoot()
					self.bullet_sprites.add(bullet)
					self.sprites.add(bullet)

			if event.type == pygame.KEYUP:
				#Player 1
				if event.key == pygame.K_UP:
					self.rocket.engineOn = False
				if event.key == pygame.K_LEFT:
					self.rocket.turnLeft = False
				if event.key == pygame.K_RIGHT:
					self.rocket.turnRight = False
				#Player 2
				if event.key == pygame.K_w:
					self.rocket2.engineOn = False
				if event.key == pygame.K_a:
					self.rocket2.turnLeft = False
				if event.key == pygame.K_d:
					self.rocket2.turnRight = False

	def display(self, screen):
		"""Display of text on screen"""
		fuel = "Fuel: %s" % self.rocket.fuel
		font = pygame.font.SysFont("sans-serif", 30)
		fuel_text = font.render(fuel, True, WHITE)
		screen.blit(fuel_text, [20, 15])

	def logic(self, screen):
		"""Engine logic which run what is needed"""
		self.sprites.update()
		self.eventhandler()
		self.display(screen)
		for bullet in self.bullet_sprites:
			bullet.logic()
		self.rocket.logic(screen)
		self.rocket2.logic(screen)
		
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