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
	Creates a engine object to run the game.
	Engine() -> object
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

		pygame.display.update()	#Update screen

	def eventhandler(self):
		"""
		Handles all user input and custom userevents.

		eventhandler() -> none
		"""
		for event in pygame.event.get():
			if event.type == pygame.QUIT:	#Quit event
				exit()
			if event.type == ASTROID_SPAWN:	#Astroid spawn event
				self.spawn_astroid()
			if event.type == RESPAWN_PLAYER1 or event.type == RESPAWN_PLAYER2:	#Player respawn event
				self.respawn_ships()
			if event.type == SHIELD_PLAYER1:	#Shield down events
				self.player1.shield_down()
			if event.type == SHIELD_PLAYER2:
				self.player2.shield_down()
			
			if event.type == POWERUP_SPAWN and len(self.powerups) < 2:
				#Spawn powerup if 2 arent allready spawned
				poweruptype = random.choice(list(POWERUP_TYPES.keys()))
				powerup_rect = POWERUP_TYPES[poweruptype]
				self.powerups.add( PowerUp(poweruptype, POWERUP_SPAWNS[random.randint(0,7)], powerup_rect, self.spritesheet) )

			if event.type == pygame.KEYDOWN:
				#Player 1 controller
				if self.player1.invisible is False:
					if event.key == pygame.K_w: self.player1.engineOn = True
					if event.key == pygame.K_a: self.player1.turnLeft = True
					if event.key == pygame.K_d: self.player1.turnRight = True
					if event.key == pygame.K_s: self.player1.speedBreak = True
					if event.key == pygame.K_SPACE:
							#Fire gun
							bullet1 = self.player1.shoot("left")	#Left wing bullet
							bullet2 = self.player1.shoot("right")	#Right wing bullet
							self.bullet_sprites.add(bullet1)
							self.bullet_sprites.add(bullet2)
				#Player 2 controllers
				if self.player2.invisible is False:
					if event.key == pygame.K_UP:	self.player2.engineOn = True
					if event.key == pygame.K_LEFT:	self.player2.turnLeft = True
					if event.key == pygame.K_RIGHT:	self.player2.turnRight = True
					if event.key == pygame.K_DOWN: self.player2.speedBreak = True
					if event.key == pygame.K_PERIOD:
							#Fire gun
							bullet1 = self.player2.shoot("left")	#Left wing bullet
							bullet2 = self.player2.shoot("right")	#Right wing bullet
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
		"""
		Send the missile the position of the enemy player

		missile_guidance() -> none
		"""
		for bullet in self.bullet_sprites:
			if bullet.type is "missile":
				if bullet.uid is 1:	#Gives bullet player2 position
					bullet.target = self.player2.pos
				if bullet.uid is 2:	#Gives bullet player2 position
					bullet.target = self.player1.pos

	def gravity_force(self, object1, object2):
		"""
		Calculates the strenght of gravity between two objects.
		A simplified version of Newton's Law of Universal Gravitation.

		gravity_force(object1, object2) -> float

		Parameters
		----------
		object1 : object
			Object with mass and position attribute.
		object2 : object
			Object with mass and position attribute.
		"""
		distance = (object1.pos - object2.pos).magnitude()		#Distance between the objects
		force = (object1.mass * object2.mass) / (distance ** 2)	#The force of gravity
		return force

	def gravity_field(self):
		"""
		Controls virtual gravity.
		Working on astroid and rockets with respect to planets.

		gravity_field() -> none
		"""
		#Rocket gravity
		for rocket in self.rockets:
			for planet in self.planets:
				distance = (rocket.pos - planet.pos).magnitude()
				if distance < 500:	#Only affect rocket if this is the distance
					gravity_direction = Vector2D((planet.pos.x - rocket.pos.x),(planet.pos.y - rocket.pos.y)).normalized() #Direction gravity should point
					gravity_force = gravity_direction * self.gravity_force(rocket, planet) #Vector of gravity
					rocket.speed += gravity_force #Add gravity to speed vector
					rocket.calc_angle()	#Make sure the angle is recalculated

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
		Checks if bullets has collided with anything and does the logic needed.

		bullet_impact() -> none
		"""
		for bullet in self.bullet_sprites:
			#Rocket
			for rocket in self.rockets:
				if bullet.uid != rocket.uid and pygame.sprite.collide_rect(rocket, bullet) and pygame.sprite.collide_mask(rocket, bullet):
						self.explode(rocket, 30, 25, 0)			#Create explotion on rocket and lose 25 hp.
						if rocket.dead:							#Player died
							self.give_score(bullet.uid, 100)	#Give the player that got the kill 100 in score
						self.explode(bullet, 20)				#Explode the bullet

			#Astroid
			for astroid in self.astroids:
				if pygame.sprite.collide_rect(bullet, astroid) and pygame.sprite.collide_mask(bullet, astroid):
					astroid.life -=1					#Astroid loses health
					self.explode(bullet, 20)			#Explode bullet
					if astroid.life is 0:				#Astroid is killed
						self.give_score(bullet.uid, 10)	#Give score to player
						self.explode(astroid, 75)		#Explode astroid

			#Planet
			for planet in self.planets:
				if pygame.sprite.collide_rect(planet, bullet) and pygame.sprite.collide_mask(planet, bullet):
					self.explode(bullet, 20)			#Explode bullet

			#Platform
			for platform in self.platforms:
				if bullet.uid is not platform.uid and pygame.sprite.collide_rect(platform, bullet) and pygame.sprite.collide_mask(platform, bullet):
					self.explode(bullet, 20)			#Explode bullet

	def environment_impact(self):
		"""
		Collision detection between astroids, planets, ships and platforms.

		environment_impact() -> none
		"""
		for astroid in self.astroids:
			#Astroid -> Planet
			for planet in self.planets:
				if pygame.sprite.collide_rect(astroid, planet) and pygame.sprite.collide_mask(astroid, planet):
					self.explode(astroid, 30)			#Explode astroid

			#Astroid -> Ship
			for rocket in self.rockets:
				if pygame.sprite.collide_rect(astroid, rocket) and pygame.sprite.collide_mask(astroid, rocket):
					if rocket.shield is False:	self.explode(rocket, 50, 100, 25)	#Player loses 100hp and 25score
					else:						self.explode(astroid, 30)			#Explode astroid

			#Astroid -> Astroid
			for astroid2 in self.astroids:
				if (astroid != astroid2) and pygame.sprite.collide_rect(astroid, astroid2) and (SCREEN_X -50 > astroid.rect.x > 50) and ( SCREEN_Y - 50 > astroid.rect.y > 50) and pygame.sprite.collide_mask(astroid, astroid2):
					self.destroy_astroid(astroid, astroid2)		#Explode astroid
					
			#Astroid -> Platform
			for platform in self.platforms:
				if pygame.sprite.collide_rect(astroid, platform) and pygame.sprite.collide_mask(astroid, platform):
					self.explode(astroid, 40)	#Explode astroid

		for rocket in self.rockets:
			#Ship -> Planet
			for planet in self.planets:
				if pygame.sprite.collide_rect(rocket, planet) and pygame.sprite.collide_mask(rocket, planet):
					self.explode(rocket, 50, 100, 25, True)	#-100hp, -25score and explode.

			#Ship -> Platform
			for platform in self.platforms:
				if pygame.sprite.collide_rect(rocket, platform) and pygame.sprite.collide_rect(rocket, platform) and (platform.uid == rocket.uid):
					rocket.refuel = True #Rocket is refuling
			#Ship -> Ship 
			for rocket2 in self.rockets:
				if rocket != rocket2:
					if pygame.sprite.collide_rect(rocket, rocket2) and pygame.sprite.collide_mask(rocket,rocket2):
						self.explode(rocket, 50, 1000, 50) #-1000hp, -50score and explode.
						self.explode(rocket2, 50, 1000, 50) #-1000hp, -50score and explode.

			#Ship -> Powerup
			for powerup in self.powerups:
				if pygame.sprite.collide_rect(rocket, powerup) and pygame.sprite.collide_rect(rocket,powerup) and rocket.dead is False:
					if powerup.type is "hp": rocket.health += HP_INCREASE		#HP powerup, increase health
					if powerup.type is "missile": rocket.missiles += MISSILES 	#Give player missiles
					if powerup.type is "shield":								#Give player shield
						rocket.shield_up()
					self.powerups.remove(powerup)								#Remove powerup

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
			if kill:	#If kill is passed we kill it
				self.explotions.add( Explotion(obj.rect.centerx, obj.rect.centery, explotionsize) )
				obj.score -=scoreloss
				obj.dead = True
			else:
				if obj.shield is False:	#Make sure the player does not have a shield
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
		if astroid1.mass > astroid2.mass:	#If left is bigger than right
			if astroid2.type is 2: self.explode(astroid2, 50)
			if astroid2.type is 3: self.explode(astroid2, 30)
		elif astroid1.mass < astroid2.mass:	#If right is bigger than left
			if astroid1.type is 2: self.explode(astroid1, 50)
			if astroid1.type is 3: self.explode(astroid2, 30)
		else:								#If same size
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
		if len(self.astroids) < MAX_ASTROIDS:	#Create astroids if we dont have enough
			astroid = Astroid(	ASTROID_SPAWNS[random.randint(0,7)],
								random.choice([ASTROID_1, ASTROID_2, ASTROID_3]),
								self.spritesheet  )
			self.astroids.add(astroid)
	
	def spawn_powerups(self):
		"""
		Starts a timer to spawn powerups.

		spawn_powerups() -> none
		"""
		if len(self.powerups) == 0: 
			pygame.time.set_timer(POWERUP_SPAWN, 10000)


	def render_text(self, screen, pos, message):
		"""
		Method to render text.

		render_text(screen, pos, message) -> none

		Parameters
		----------
		screen : screen object
		pos : touple
		message : string
		"""
		font = pygame.font.SysFont("sans-serif", 22)	#Font object
		text = font.render(message, True, WHITE)		#Text object
		screen.blit(text, pos)							#Blit on position

	### HUD TEXT ###
	def stats(self, screen):
		"""
		Display all stats on hud.

		stats(screen) -> none
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
	main() -> none
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