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
from staticobjects import *
from astroid import *
from planet import *

class Engine:
	"""This is the engine class"""
	def __init__(self):
		self.players = 2

		self.bg = pygame.sprite.Group()
		self.hud = pygame.sprite.Group()
		self.rockets = pygame.sprite.Group()
		self.explotions = pygame.sprite.Group()
		self.bullet_sprites = pygame.sprite.Group()
		self.platforms = pygame.sprite.Group()
		self.planets = pygame.sprite.Group()
		self.astroids = pygame.sprite.Group()

		self.generate_player() #Generate all players
		self.generate_planets()
		self.bg.add(Background())
		self.hud.add(Hud())

	def generate_player(self):
		"""generates players"""
		#Generate ships
		for i in range(1,self.players+1):
			rocket = Rocket(i)
			self.rockets.add(rocket)

		#Generate platform for players
		for i in range(1,self.players+1):
			platform = Platform(i)
			self.platforms.add(platform)

	def generate_planets(self):
		self.planets.add(Planet((200,200),TIGER_PLANET))
		self.planets.add(Planet((900,500),BLACK_HOLE))
		
	def generate_astroid(self):
		if len(self.astroids)<6:
			self.astroids.add(
					Astroid(
						random.choice([(-10,SCREEN_Y/2),(SCREEN_X/2, SCREEN_Y+10),(300,SCREEN_Y+10),(300,-10)]),
						random.choice([ASTROID_1, ASTROID_2, ASTROID_3])
					)
				)

	def gravity_field(self):
		for rocket in self.rockets:
			for planet in self.planets:
				if (rocket.pos - planet.pos).magnitude() < 200:
					gravity_vector = Vector2D((planet.pos.x-rocket.pos.x),(planet.pos.y - rocket.pos.y))
					rocket.pos += gravity_vector/100

		for astroid in self.astroids:
			for planet in self.planets:
				distance = (astroid.pos - planet.pos).magnitude()
				if  distance < 300:
					gravity_vector = Vector2D(
										(planet.pos.x - astroid.pos.x),
										(planet.pos.y - astroid.pos.y)
									)
					astroid.speed += (gravity_vector/35) / distance

	def eventhandler(self):
		"""The eventhandler"""
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit()

			if event.type == pygame.USEREVENT:
				self.generate_astroid()
			
			if event.type == pygame.KEYDOWN:
				#Player 1
				for rocket in self.rockets:
					if rocket.uid == 1:
						if event.key == pygame.K_w:
							rocket.engineOn = True
						if event.key == pygame.K_a:
							rocket.turnLeft = True
						if event.key == pygame.K_d:
							rocket.turnRight = True
						if event.key == pygame.K_SPACE:
							bullet = rocket.shoot()
							self.bullet_sprites.add(bullet)

					if rocket.uid == 2:
						if event.key == pygame.K_UP:
							rocket.engineOn = True
						if event.key == pygame.K_LEFT:
							rocket.turnLeft = True
						if event.key == pygame.K_RIGHT:
							rocket.turnRight = True
						if event.key == pygame.K_RSHIFT:
							bullet = rocket.shoot()
							self.bullet_sprites.add(bullet)
					

			if event.type == pygame.KEYUP:
				for rocket in self.rockets:
					#Player 1
					if rocket.uid == 1:
						if event.key == pygame.K_w:
							rocket.engineOn = False
						if event.key == pygame.K_a:
							rocket.turnLeft = False
						if event.key == pygame.K_d:
							rocket.turnRight = False

					#Player 2
					if rocket.uid == 2:
						if event.key == pygame.K_UP:
							rocket.engineOn = False
						if event.key == pygame.K_LEFT:
							rocket.turnLeft = False
						if event.key == pygame.K_RIGHT:
							rocket.turnRight = False

	def platform_impact(self):
		"""Checks if rocket collide with platform"""
		for rocket in self.rockets:
			for platform in self.platforms:
				hit = pygame.sprite.collide_rect(rocket, platform)
				if hit:
					rocket.refuel = True

	def bullet_impact(self):
		"""Checks if sprites collide"""
		for rocket in self.rockets:
			#Bullets and rocket
			collide_rocket = pygame.sprite.spritecollide(rocket,self.bullet_sprites,False)
			for bullet in collide_rocket:
				if bullet.uid != rocket.uid and pygame.sprite.collide_mask(rocket, bullet):
					rocket.bullet_impact()
					#Mini explotion
					explotion = Explotion(bullet.rect.centerx, bullet.rect.centery, 30)
					self.explotions.add(explotion)
					if rocket.health <= 0:
						explotion = Explotion(rocket.rect.centerx, rocket.rect.centery, 75)
						self.explotions.add(explotion)
						rocket.respawn()
						for rocket in self.rockets:
							if rocket.uid is bullet.uid:
								rocket.score += 100 #Give the player who got the hit score
					self.bullet_sprites.remove(bullet)
		
		#Astroid collide with bullet
		for astroid in self.astroids:
			for bullet in self.bullet_sprites:
				hit = pygame.sprite.collide_rect(astroid, bullet)
				if hit and pygame.sprite.collide_mask(astroid, bullet):
					explotion = Explotion(bullet.rect.centerx, bullet.rect.centery, 20)
					self.explotions.add(explotion)
					self.bullet_sprites.remove(bullet)

		#Planet collide with bullet
		for planet in self.planets:
			for bullet in self.bullet_sprites:
				hit = pygame.sprite.collide_rect(planet, bullet)
				if hit and pygame.sprite.collide_mask(planet, bullet):
					explotion = Explotion(bullet.rect.centerx, bullet.rect.centery, 20)
					self.explotions.add(explotion)
					self.bullet_sprites.remove(bullet)

	def bullet_out_of_screen(self):
		for bullet in self.bullet_sprites:
			#Venstre vegg	
			if bullet.pos.x <= 0:
				self.bullet_sprites.remove(bullet)
			#Høyre vegg
			if bullet.pos.x >= SCREEN_X:
				self.bullet_sprites.remove(bullet)
			#Tak
			if bullet.pos.y <= 0:
				self.bullet_sprites.remove(bullet)
			#Bunn
			if bullet.pos.y >= SCREEN_Y:
				self.bullet_sprites.remove(bullet)

	def environment_impact(self):
		for astroid in self.astroids:
			#Astroid collide with planet
			for planet in self.planets:
				hit = pygame.sprite.collide_rect(astroid, planet)
				if hit and pygame.sprite.collide_mask(astroid, planet):
					explotion = Explotion(astroid.rect.centerx, astroid.rect.centery, 30)
					self.explotions.add(explotion)
					self.astroids.remove(astroid)
			#Astroid collide with rocket
			for rocket in self.rockets:
				hit = pygame.sprite.collide_rect(astroid, rocket)
				if hit and pygame.sprite.collide_mask(astroid, rocket):
					explotion = Explotion(rocket.rect.centerx, rocket.rect.centery, 30)
					self.explotions.add(explotion)
					rocket.respawn()
			#Astroid collide with astroid
			for astroid2 in self.astroids:
				hit = pygame.sprite.collide_rect(astroid, astroid2)
				if hit and (astroid != astroid2) and (SCREEN_X -50 > astroid.rect.x > 50) and ( SCREEN_Y - 50 > astroid.rect.y > 50) and pygame.sprite.collide_mask(astroid, astroid2):
					explotion = Explotion(astroid.rect.centerx, astroid.rect.centery, 30)
					explotion2 = Explotion(astroid2.rect.centerx, astroid2.rect.centery, 30)
					self.explotions.add(explotion)
					self.explotions.add(explotion2)
					self.astroids.remove(astroid)
					self.astroids.remove(astroid2)

		for rocket in self.rockets:
			#Rocket collide with platform
			for platform in self.platforms:
				hit = pygame.sprite.collide_rect(rocket, platform)
				if hit:
					rocket.refuel = True
			#Rocket collide with planet
			for planet in self.planets:
				hit = pygame.sprite.collide_rect(rocket, planet)
				if hit and pygame.sprite.collide_mask(rocket, planet):
					explotion = Explotion(rocket.rect.centerx, rocket.rect.centery, 30)
					self.explotions.add(explotion)
					rocket.respawn()



	def display(self, screen):
		"""Display of text on screen"""
		
			#FUEL DISPLAY
		for rocket in self.rockets:
			fuel = "%s" % int(rocket.fuel/10)
			font = pygame.font.SysFont("sans-serif", 22)
			fuel_text = font.render(fuel, True, RED)
			
			if rocket.uid == 1:
				fuel_text = font.render(fuel, True, WHITE)
				screen.blit(fuel_text, [105, 30])
			else: 
				fuel_text = font.render(fuel, True, WHITE)
				screen.blit(fuel_text, [SCREEN_X-155, 30])

			#SCORE DISPLAY
		for rocket in self.rockets:
			score = "%s" % rocket.score
			font = pygame.font.SysFont("sans.serif", 22)
			score_text = font.render(score, True, RED)

			if rocket.uid == 1:
				score_text = font.render(score,True,WHITE)
				screen.blit(score_text, [200, 30])
			else:
				score_text = font.render(score,True,WHITE)
				screen.blit(score_text, [SCREEN_X - 60, 30])

			#HEALTH DISPLAY
		for rocket in self.rockets:
			health = "%s" % rocket.health
			font = pygame.font.SysFont("sans.serif", 22)
			health_text = font.render(health, True, WHITE)

			if rocket.uid == 1:
				health_text = font.render(health, True, WHITE)
				screen.blit(health_text,[20,30])
			else:
				health_text = font.render(health, True, WHITE)
				screen.blit(health_text, [SCREEN_X-240, 30])


	def logic(self, screen):
		"""Engine logic which run what is needed"""
		self.eventhandler()

		#Update
		self.bg.update()
		self.hud.update()
		self.explotions.update()
		self.rockets.update()
		self.bullet_sprites.update()
		self.platforms.update()
		self.planets.update()
		self.astroids.update()

		#Colision detect
		self.platform_impact()
		self.bullet_impact()
		self.gravity_field()
		self.environment_impact()
		self.bullet_out_of_screen()

		#Drawing
		self.bg.draw(screen)				#Draw background sprite
		self.bullet_sprites.draw(screen)	#Draw bullet sprites
		self.platforms.draw(screen)			#Draw platform sprites
		self.rockets.draw(screen)			#Draw rocket sprites
		self.planets.draw(screen)
		self.astroids.draw(screen)
		self.explotions.draw(screen)		#Draw explotions
		self.hud.draw(screen)				#Draw background sprite
		self.display(screen)				#Draw hud

		#Remove explotion when animation is over
		for explotion in self.explotions:
			if explotion.kill:
				self.explotions.remove(explotion)

		pygame.display.update()

def main():
	"""runs the program"""
	pygame.init()
	pygame.display.set_caption("Mayhem")
	#screen = pygame.display.set_mode((SCREEN),pygame.FULLSCREEN)	#FULLSCREEN
	screen = pygame.display.set_mode((SCREEN), 0, 32 )				#WINDOWED
	clock = pygame.time.Clock()
	engine = Engine() #Initialize game engine
	pygame.time.set_timer(pygame.USEREVENT, 3000)#Set a timer for spawning astroids

	
	while True:	
		time = clock.tick(FPS)
		engine.logic(screen)

if __name__ == "__main__":
	main()