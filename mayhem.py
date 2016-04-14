"""
###Space Lazer Wars###
This is a 2 player arcade shooting game where both players 
control a rocket and try to shoot eachother with bullets.

Created by:
Lars Karlsen and Mellet Solbakk
"""

#!/usr/bin/env python3
import pygame
import random
import math
import cProfile
from config import *
from gameconstants import *
from config import *
from Vector2D import *
from movingobject import *
from staticobject import *
from ui import *
from astroid import *
from planet import *
from rocket import *
from bullet import *
from powerup import *

class Engine:
	"""
	Engine class to initialize all game assets and instance variables.
	"""

	def __init__(self):
		self.players = 2
		self.bg = pygame.sprite.Group()				#Background sprite
		self.hud = pygame.sprite.Group()			#HUD sprite
		self.rockets = pygame.sprite.Group()		#Rocket sprites
		self.explotions = pygame.sprite.Group()		#Explotion sprites
		self.bullet_sprites = pygame.sprite.Group()	#Bullet sprites
		self.platforms = pygame.sprite.Group()		#Platform sprites
		self.powerups = pygame.sprite.Group()		#Powerup sprites
		self.planets = pygame.sprite.Group()		#Planet sprites
		self.astroids = pygame.sprite.Group()		#Astroid sprites
		self.spritesheet = Spritesheet("sprites/spritesheet.png")

		#Create players
		self.player1 = Rocket(1, self.spritesheet, RED_ENGINE_OFF, PLAYER1_SPAWN)
		self.player2 = Rocket(2, self.spritesheet, BLUE_ENGINE_OFF, PLAYER2_SPAWN)
		self.rockets.add(self.player1)	#Player1
		self.rockets.add(self.player2)	#Player2
		self.planets.add(Planet((SCREEN_X/2,SCREEN_Y/2),BLACK_HOLE,self.spritesheet))	#Add our black hole.

		self.generate_platforms()					#Generate platforms
		self.spawn_powerups()						#Generate powerup
		self.bg.add(Background())					#Add background
		self.hud.add(Hud())							#Add hud

	def logic(self, screen):
		"""
		Logic method that runs all the engines methods needed for each frame.

		login(Screen) -> none
		"""
		self.eventhandler()				#Handle game events
		self.missile_guidance()			#Give missiles coordinates of target ship

		#Update all spritegroups
		self.bg.update()
		self.hud.update()
		self.explotions.update()
		self.rockets.update()
		self.powerups.update()
		self.bullet_sprites.update()
		self.platforms.update()
		self.planets.update()
		self.astroids.update()

		#Collision detection and misc methods
		self.gravity_field()
		self.bullet_impact()
		self.environment_impact()
		self.bullet_out_of_screen()

		#Drawing
		self.bg.draw(screen)				#Draw background sprite
		self.platforms.draw(screen)			#Draw platform sprites
		self.bullet_sprites.draw(screen)	#Draw bullet sprites
		self.powerups.draw(screen)			#Draw powerup sprites
		self.rockets.draw(screen)			#Draw rocket sprites
		self.planets.draw(screen)			#Draw planets
		self.astroids.draw(screen)			#Draw astroids
		self.explotions.draw(screen)		#Draw explotions
		self.hud.draw(screen)				#Draw hud background
		self.stats(screen)					#Draw stats 

		#Remove explotion when animation is over
		for explotion in self.explotions:
			if explotion.kill:
				self.explotions.remove(explotion)

		pygame.display.update()

	def eventhandler(self):
		"""
		Handles all user input and custom userevents.
		"""
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit()
			if event.type == ASTROID_SPAWN:
				self.spawn_astroid()
			if event.type == RESPAWN_PLAYER1 or event.type == RESPAWN_PLAYER2:
				self.respawn_ships()
			if event.type == ASTROID_SPAWN:
				self.spawn_astroid()
			if event.type == SHIELD_PLAYER1:
				self.player1.shield_down()
			if event.type == SHIELD_PLAYER2:
				self.player2.shield_down()
			
			if event.type == POWERUP_SPAWN and len(self.powerups) < 2:
				poweruptype = random.choice(list(POWERUP_TYPES.keys()))
				powerup_rect = POWERUP_TYPES[poweruptype]
				self.powerups.add( PowerUp(poweruptype, POWERUP_SPAWNS[random.randint(0,7)], powerup_rect, self.spritesheet) )

			if event.type == pygame.KEYDOWN:
				#Player 1
				if self.player1.invisible is False:
					if event.key == pygame.K_w: self.player1.engineOn = True
					if event.key == pygame.K_a: self.player1.turnLeft = True
					if event.key == pygame.K_d: self.player1.turnRight = True
					if event.key == pygame.K_s: self.player1.speedBreak = True
					if event.key == pygame.K_SPACE:
							bullet1 = self.player1.shoot("left")
							bullet2 = self.player1.shoot("right")
							self.bullet_sprites.add(bullet1)
							self.bullet_sprites.add(bullet2)
				#Player 2
				if self.player2.invisible is False:
					if event.key == pygame.K_UP:	self.player2.engineOn = True
					if event.key == pygame.K_LEFT:	self.player2.turnLeft = True
					if event.key == pygame.K_RIGHT:	self.player2.turnRight = True
					if event.key == pygame.K_DOWN: self.player2.speedBreak = True
					if event.key == pygame.K_PERIOD:
							bullet1 = self.player2.shoot("left")
							bullet2 = self.player2.shoot("right")
							self.bullet_sprites.add(bullet1)
							self.bullet_sprites.add(bullet2)

			if event.type == pygame.KEYUP:
				if event.key == pygame.K_w: self.player1.engineOn = False
				if event.key == pygame.K_a: self.player1.turnLeft = False
				if event.key == pygame.K_d: self.player1.turnRight = False
				if event.key == pygame.K_s: self.player1.speedBreak = False

				if event.key == pygame.K_UP: self.player2.engineOn = False
				if event.key == pygame.K_LEFT: self.player2.turnLeft = False
				if event.key == pygame.K_RIGHT: self.player2.turnRight = False
				if event.key == pygame.K_DOWN: self.player2.speedBreak = False

	def missile_guidance(self):
		for bullet in self.bullet_sprites:
			if bullet.type is "missile":
				if bullet.uid is 1:
					bullet.target = self.player2.pos
				if bullet.uid is 2:
					bullet.target = self.player1.pos

	def gravity_force(self, object1, object2):
		"""
		Calculates the strenght of gravity between two objects.
		A simplified version of Newton's Law of Universal Gravitation.
		"""
		distance = (object1.pos - object2.pos).magnitude()
		force = (object1.mass * object2.mass) / (distance ** 2)
		return force

	def gravity_field(self):
		"""
		Controls virtual gravity from planets.
		Working on astroids and rockets.
		"""
		#Rocket gravity
		for rocket in self.rockets:
			for planet in self.planets:
				distance = (rocket.pos - planet.pos).magnitude()
				if distance < 500:
					gravity_direction = Vector2D((planet.pos.x - rocket.pos.x),(planet.pos.y - rocket.pos.y)).normalized()
					gravity_force = gravity_direction * self.gravity_force(rocket, planet)
					rocket.speed += gravity_force
					rocket.calc_angle()

		#Astroid gravity
		for astroid in self.astroids:
			for planet in self.planets:
				distance = (astroid.pos - planet.pos).magnitude()
				if  distance < 700:
					gravity_direction = Vector2D((planet.pos.x - astroid.pos.x),(planet.pos.y - astroid.pos.y)).normalized()
					gravity_force = gravity_direction * self.gravity_force(astroid, planet)
					astroid.speed += gravity_force
			
	def bullet_impact(self):
		"""
		Check if any bullet has collided with a rocket, platform, planet or a astroid.
		"""
		for bullet in self.bullet_sprites:
			#Rocket
			for rocket in self.rockets:
				if bullet.uid != rocket.uid and pygame.sprite.collide_rect(rocket, bullet) and pygame.sprite.collide_mask(rocket, bullet):
						self.explode(rocket, 75, 25, 0)
						if rocket.dead:
							self.give_score(bullet.uid, 100)
						self.explode(bullet, 20)

			#Astroid
			for astroid in self.astroids:
				if pygame.sprite.collide_rect(bullet, astroid):
					if pygame.sprite.collide_mask(bullet, astroid):
						astroid.life -=1
						self.explode(bullet, 20)
						if astroid.life is 0: #Astroid is killed
							self.give_score(bullet.uid, 10)
							self.explode(astroid, 75)

			#Planet
			for planet in self.planets:
				if pygame.sprite.collide_rect(planet, bullet):
					if pygame.sprite.collide_mask(planet, bullet):
						self.explode(bullet, 20)

			#Platform
			for platform in self.platforms:
				if pygame.sprite.collide_rect(platform, bullet):
					if pygame.sprite.collide_mask(platform, bullet) and bullet.uid is not platform.uid:
						self.explode(bullet, 20)

	def environment_impact(self):
		"""
		Colision detection between astroids, planets, ships and platforms.
		"""
		for astroid in self.astroids:
			#Astroid -> Planet
			for planet in self.planets:
				if pygame.sprite.collide_rect(astroid, planet):
					if pygame.sprite.collide_mask(astroid, planet):
						self.explode(astroid, 30)

			#Astroid -> Ship
			for rocket in self.rockets:
				if pygame.sprite.collide_rect(astroid, rocket):
					if pygame.sprite.collide_mask(astroid, rocket):
						if rocket.shield is False:	self.explode(rocket, 50, 100, 10) #-100hp, -20score
						else:						self.explode(astroid, 30)

			#Astroid -> Astroid
			for astroid2 in self.astroids:
				if (astroid != astroid2) and pygame.sprite.collide_rect(astroid, astroid2):
					if (SCREEN_X -50 > astroid.rect.x > 50) and ( SCREEN_Y - 50 > astroid.rect.y > 50) and pygame.sprite.collide_mask(astroid, astroid2):
						self.destroy_astroid(astroid, astroid2)
					
			#Astroid -> Platform
			for platform in self.platforms:
				if pygame.sprite.collide_rect(astroid, platform):
					if pygame.sprite.collide_mask(astroid, platform):
						self.explode(astroid, 40)

		for rocket in self.rockets:
			#Ship -> Planet
			for planet in self.planets:
				if pygame.sprite.collide_rect(rocket, planet):
					if pygame.sprite.collide_mask(rocket, planet):
						self.explode(rocket, 50, 100, 20, True)	#-100hp, -20score and explode.

			#Ship -> Platform
			for platform in self.platforms:
				if pygame.sprite.collide_rect(rocket, platform):
					if pygame.sprite.collide_rect(rocket, platform) and (platform.uid == rocket.uid):
						rocket.refuel = True
			#Ship -> Ship 
			for rocket2 in self.rockets:
				if rocket != rocket2:
					if pygame.sprite.collide_rect(rocket, rocket2):
						if pygame.sprite.collide_mask(rocket,rocket2):
							self.explode(rocket, 50, 1000, 50) #-1000hp, -50score and explode.
							self.explode(rocket2, 50, 1000, 50) #-1000hp, -50score and explode.

			#Ship -> Powerup
			for powerup in self.powerups:
				if pygame.sprite.collide_rect(rocket, powerup):
					if pygame.sprite.collide_rect(rocket,powerup) and rocket.dead is False:
						if powerup.type is "hp": rocket.health += HP_INCREASE
						if powerup.type is "missile": rocket.missiles += MISSILES
						if powerup.type is "shield":
							rocket.shield_up()
						self.powerups.remove(powerup)

	def explode(self, obj, explotionsize, hploss = None, scoreloss = None, kill = False):
		"""
		Kills and adds a explotion to the objects position.
		If the object is a player it will not remove it, only take away hp.
		This method also checks if the player has a shield.

		explode(obj, explotionsize, hploss) -> none

		Parameters
		----------
		obj : object
			Object to get the position to create a explotion.
		explotionsize : int
			The size of the explotion.
		hploss : int, optional
			Change in hp for a player object.
		scoreloss : int, optional
			Change in score a player object.
		kill : bool, optional
			Pass in to kill no matter what.
			(Used to kill a player if it collides with a planet, even if it has a shield.)

		Examples
		--------
		Exploding and removing a bullet: explode(bullet, 50, True)
		Exploding and killing a player with no score loss: explode(player, 50, 100, 0)
		Killing a player no matter what: explode(player, 50, 0, 0, True)
		"""
		#If the passed in object is a player
		if hasattr(obj, 'shield'):
			if kill:
				self.explotions.add( Explotion(obj.rect.centerx, obj.rect.centery, explotionsize) )
				obj.score -=scoreloss
				obj.dead = True
			else:
				if obj.shield is False:
					self.explotions.add( Explotion(obj.rect.centerx, obj.rect.centery, explotionsize) )
					obj.health -= hploss
					obj.score -= scoreloss
					if obj.health <= 0: obj.dead = True
		#Object is a astroid or a bullet
		else:
			self.explotions.add( Explotion(obj.rect.centerx, obj.rect.centery, explotionsize) )
			obj.kill()
			

	def give_score(self, playerid, score):
		"""
		Give a playerid score.

		give_score(playerid, score) -> none

		Parameters
		----------
		playerid : int
			Userid to give score.
		score : int
			Ammoutn of score.

		Examples
		--------
		Give player1 50 in score: give_score(1, 50)
		"""
		if playerid is 1: self.player1.score += score
		if playerid is 2: self.player2.score += score

	def destroy_astroid(self, astroid1, astroid2):
		"""
		Takes in two astroid objects and decides who will be destroyed.
		Destroyes the smallest, or if the same size both.

		destroy_astroid(astroid1, astroid2) -> none

		Parameters
		----------
		astroid1 : astroid object
		astroid2 : astroid object
		"""
		if astroid1.mass > astroid2.mass:
			if astroid2.type is 2: self.explode(astroid2, 50)
			if astroid2.type is 3: self.explode(astroid2, 30)
		elif astroid1.mass < astroid2.mass:
			if astroid1.type is 2: self.explode(astroid1, 50)
			if astroid1.type is 3: self.explode(astroid2, 30)
		else:
			self.explode(astroid1, 50)
			self.explode(astroid2, 50)

	def bullet_out_of_screen(self):
		"""
		Removed bullets that exit the screen

		bullet_out_of_screen() -> none
		"""
		for bullet in self.bullet_sprites:
			if bullet.pos.x <= 0:			self.bullet_sprites.remove(bullet)	#Left wall
			if bullet.pos.x >= SCREEN_X:	self.bullet_sprites.remove(bullet)	#Right wall
			if bullet.pos.y <= 0:			self.bullet_sprites.remove(bullet)	#Roof
			if bullet.pos.y >= SCREEN_Y:	self.bullet_sprites.remove(bullet)	#Floor

	def generate_platforms(self):
		"""
		Generates platforms for every player in the player group.

		generate_platforms() -> none
		"""
		for rocket in self.rockets:
			platform = Platform(rocket.uid, self.spritesheet)
			self.platforms.add(platform)

	def respawn_ships(self):
		"""
		Respawnes a ship if it is set to invisible.

		respawn_ships() -> none
		"""
		if self.player1.invisible: self.player1.respawn()
		if self.player2.invisible: self.player2.respawn()
		
	def spawn_astroid(self):
		"""
		Spawns a astroid if the limit of astroids is not exceeded.

		spawn_astroid() -> none
		"""
		if len(self.astroids) < 8:
			astroid = Astroid(	ASTROID_SPAWNS[random.randint(0,7)],
								random.choice([ASTROID_1, ASTROID_2, ASTROID_3]),
								self.spritesheet  )
			self.astroids.add(astroid)
	
	def spawn_powerups(self):
		"""
		Spawns powerups 20s. When a powerup is taken, a new one spawns 20s later.
		"""
		if len(self.powerups) == 0: 
			pygame.time.set_timer(POWERUP_SPAWN, 10000)


	def render_text(self, screen, pos, message):
		"""
		Method to render text.
		Takes in screen, pos(tuple), message(string) as parameter.
		render_text(screen, (x,y), "message")
		"""
		font = pygame.font.SysFont("sans-serif", 22)
		text = font.render(message, True, WHITE)
		screen.blit(text, pos)

	### HUD TEXT ###
	def stats(self, screen):
		"""
		Display stats on the hud for the ships.
		"""
		for rocket in self.rockets:
			fuel = "%s" % int(rocket.fuel/10)						#TEXT FOR FUEL
			score = "%s" % rocket.score 							#TEXT FOR SCORE
			health = "%s" % rocket.health 							#TEXT FOR HEALTH

			if rocket.uid is 1:
				self.render_text(screen, (105,30), fuel)			#FUEL
				self.render_text(screen, (200,30), score)			#SCORE
				self.render_text(screen, (20,30), health)			#HEALTH
			else:
				self.render_text(screen, (SCREEN_X-155,30), fuel)	#FUEL
				self.render_text(screen, (SCREEN_X-60,30), score)	#SCORE
				self.render_text(screen, (SCREEN_X-240,30), health)	#HEALTH

def main():
	"""
	Creates a screen, clock, creates a instance of the engine and starts the game loop.
	"""
	pygame.init()
	pygame.display.set_caption("Space Lazer Wars")
	screen = pygame.display.set_mode((SCREEN), 0, 32)
	clock = pygame.time.Clock()
	engine = Engine() #Initialize game engine

	pygame.time.set_timer(ASTROID_SPAWN, 1500) #Set a timer for spawning astroids

	while True:	
		clock.tick(FPS)
		engine.logic(screen)

if __name__ == "__main__":
	main()