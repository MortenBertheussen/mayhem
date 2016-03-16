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
		self.rockets = []
		self.obstacle = []
		self.players = 2
		self.spawn1 = Vector2D(10,SCREEN_Y/2)
		self.spawn2 = Vector2D(SCREEN_X-10, SCREEN_Y/2)

		self.obstacle_sprites = pygame.sprite.Group()
		self.bullet_sprites = pygame.sprite.Group()
		self.sprites = pygame.sprite.Group()

		self.generate_player() #Generate all players

	def generate_player(self):
		for i in range(1,self.players+1):
			rocket = Rocket(i)
			self.rockets.append(rocket)
			self.sprites.add(rocket)

	def eventhandler(self):
		"""The eventhandler"""
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit()
			
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_q:
					exit()
				#Player 1
				for rocket in self.rockets:
					if rocket.uid == 1:
						if event.key == pygame.K_UP:
							rocket.engineOn = True
						if event.key == pygame.K_LEFT:
							rocket.turnLeft = True
						if event.key == pygame.K_RIGHT:
							rocket.turnRight = True
						if event.key == pygame.K_KP_ENTER:
							bullet = rocket.shoot()
							self.bullet_sprites.add(bullet)
							self.sprites.add(bullet)
					if rocket.uid == 2:
						if event.key == pygame.K_w:
							rocket.engineOn = True
						if event.key == pygame.K_a:
							rocket.turnLeft = True
						if event.key == pygame.K_d:
							rocket.turnRight = True
						if event.key == pygame.K_SPACE:
							bullet = rocket.shoot()
							self.bullet_sprites.add(bullet)
							self.sprites.add(bullet)

			if event.type == pygame.KEYUP:
				for rocket in self.rockets:
					#Player 1
					if rocket.uid == 1:
						if event.key == pygame.K_UP:
							rocket.engineOn = False
						if event.key == pygame.K_LEFT:
							rocket.turnLeft = False
						if event.key == pygame.K_RIGHT:
							rocket.turnRight = False
					#Player 2
					if rocket.uid == 2:
						if event.key == pygame.K_w:
							rocket.engineOn = False
						if event.key == pygame.K_a:
							rocket.turnLeft = False
						if event.key == pygame.K_d:
							rocket.turnRight = False

	def bullet_impact(self):
		for rocket in self.rockets:
			collide_rocket = pygame.sprite.spritecollide(rocket,self.bullet_sprites,False)
			for bullet in collide_rocket:
				if bullet.uid != rocket.uid:
					rocket.pos = self.spawn1


	def display(self, screen):
		"""Display of text on screen"""
		fuel = "Fuel: %s" % self.rocket.fuel
		font = pygame.font.SysFont("sans-serif", 30)
		fuel_text = font.render(fuel, True, RED)
		screen.blit(fuel_text, [20, 15])

		fuel2 = "Fuel: %s" % self.rocket2.fuel
		font2 = pygame.font.SysFont("sans-serif", 30)
		fuel2_text = font2.render(fuel2, True, BLUE)
		screen.blit(fuel2_text, [SCREEN_X-130, 15])


	def logic(self, screen):
		"""Engine logic which run what is needed"""
		self.sprites.update()
		self.eventhandler()
		#self.display(screen)

		for bullet in self.bullet_sprites:
			bullet.logic()

		for rocket in self.rockets:
			rocket.logic(screen)

		self.bullet_impact()
		
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