"""This is a 2 player arcade shooting game where both players 
control a rocket and try to shoot eachother with bullets."""

#!/usr/bin/env python3
import pygame
import random
import math
import cProfile
from gameconstants import *
from Vector2D import *
from movingobject import *
from staticobjects import *
from astroid import *
from planet import *
from rocket import *
from bullet import *
from powerup import *

ASTROID_SPAWN = pygame.USEREVENT + 1
RESPAWN_TIMER = pygame.USEREVENT + 2
POWERUP_SPAWN = pygame.USEREVENT + 3

class Engine:
	"""
	Engine class to iniziale all game assets and variables.
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
		self.player1 = Rocket(1, self.spritesheet)
		self.player2 = Rocket(2, self.spritesheet)
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
		Takes in a screen as a parameter to draw the game.
		Engine.login(screen)
		"""
		self.eventhandler()				#Handle game events
		self.missile_guidance()			#Give missiles coordinates of target ship

		#Update all spritegroups
		self.bg.update()
		self.hud.update()
		self.explotions.update()
		self.rockets.update()
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
			if event.type == pygame.QUIT: exit()					#Exit when clicking to close window			if event.type == ASTROID_SPAWN: self.spawn_astroid()	#EVENT FOR SPAWNING NEW ASTROIDS
			if event.type == RESPAWN_TIMER: self.respawn_ships()	#Event for respawning dead ships
			if event.type == ASTROID_SPAWN: self.spawn_astroid()	#Event for respawning dead ships
			
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
						if self.player1.missiles > 0:
							bullet = self.player1.shoot(1)
							self.bullet_sprites.add(bullet)
						else:
							bullet1 = self.player1.shoot(1)
							bullet2 = self.player1.shoot(2)
							self.bullet_sprites.add(bullet1)
							self.bullet_sprites.add(bullet2)
				#Player 2
				if self.player2.invisible is False:
					if event.key == pygame.K_UP:	self.player2.engineOn = True
					if event.key == pygame.K_LEFT:	self.player2.turnLeft = True
					if event.key == pygame.K_RIGHT:	self.player2.turnRight = True
					if event.key == pygame.K_DOWN: self.player2.speedBreak = True
					if event.key == pygame.K_PERIOD:
						if self.player2.missiles > 0:
							bullet = self.player2.shoot(1)
							self.bullet_sprites.add(bullet)
						else:
							bullet1 = self.player2.shoot(1)
							bullet2 = self.player2.shoot(2)
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
				if pygame.sprite.collide_mask(rocket, bullet) and bullet.uid != rocket.uid:
					self.explode(rocket, 75, 25, 0)
					if rocket.dead:
						self.give_score(bullet.uid, 100)
					self.explode(bullet, 20)

			#Astroid
			for astroid in self.astroids:
				if pygame.sprite.collide_mask(bullet, astroid):
					astroid.life -=1
					self.explode(bullet, 20)
					if astroid.life is 0: #Astroid is killed
						self.give_score(bullet.uid, 10)
						self.explode(astroid, 75)

			#Planet
			for planet in self.planets:
				if pygame.sprite.collide_mask(planet, bullet):
					self.explode(bullet, 20)

			#Platform
			for platform in self.platforms:
				if pygame.sprite.collide_mask(platform, bullet) and bullet.uid is not platform.uid:
					self.explode(bullet, 20)

	def environment_impact(self):
		"""
		Colision detection between astroids, planets, ships and platforms.
		"""
		for astroid in self.astroids:
			#Astroid -> Planet
			for planet in self.planets:
				if pygame.sprite.collide_mask(astroid, planet):
					self.explode(astroid, 30)

			#Astroid -> Ship
			for rocket in self.rockets:
				if pygame.sprite.collide_mask(astroid, rocket):
					if rocket.shield is False:	self.explode(rocket, 50, 100, 10) #-100hp, -20score
					else:						self.explode(astroid, 30)

			#Astroid -> Astroid
			for astroid2 in self.astroids:
				if (astroid != astroid2) and (SCREEN_X -50 > astroid.rect.x > 50) and ( SCREEN_Y - 50 > astroid.rect.y > 50) and pygame.sprite.collide_mask(astroid, astroid2):
					self.destroy_astroid(astroid, astroid2)
					
			#Astroid -> Platform
			for platform in self.platforms:
				if pygame.sprite.collide_mask(astroid, platform):
					self.explode(astroid, 40)

		for rocket in self.rockets:
			#Ship -> Planet
			for planet in self.planets:
				if pygame.sprite.collide_mask(rocket, planet):
					self.explode(rocket, 50, 100, 20, True)	#-100hp, -20score and explode.

			#Ship -> Platform
			for platform in self.platforms:
				hit = pygame.sprite.collide_rect(rocket, platform)
				if hit and (platform.uid == rocket.uid):
					rocket.refuel = True
			#Ship -> Ship 
			for rocket2 in self.rockets:
				if rocket != rocket2:
					if pygame.sprite.collide_mask(rocket,rocket2):
						self.explode(rocket, 50, 100, 50)
						self.explode(rocket2, 50, 100, 50)

			#Ship -> Powerup
			for powerup in self.powerups:
				if pygame.sprite.collide_rect(rocket,powerup) and rocket.dead is False:
					if powerup.type is "hp": rocket.health += 100
					if powerup.type is "missile": rocket.missiles += 3
					if powerup.type is "shield":
						rocket.shield = True
						rocket.shieldTimer = 0
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

		Examples
		--------
		Exploding and removing a bullet: explode(bullet, 50, True)
		Exploding and killing a player: explode(player, 50, False, -50, True)
		Exploding a player that has a shield: explode(player, 25, False, 0, False)
		"""
		#If the passed in object is a player
		if hasattr(obj, 'shield'):
			if kill:
				self.explotions.add( Explotion(obj.rect.centerx, obj.rect.centery, explotionsize) )
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
			

	def give_score(self, player, score):
		if player is 1: self.player1.score += score
		if player is 2: self.player2.score += score

	def destroy_astroid(self, astroid1, astroid2):
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
		Removed bullets if they exit the screen.
		"""
		for bullet in self.bullet_sprites:
			if bullet.pos.x <= 0:			self.bullet_sprites.remove(bullet)	#Left wall
			if bullet.pos.x >= SCREEN_X:	self.bullet_sprites.remove(bullet)	#Right wall
			if bullet.pos.y <= 0:			self.bullet_sprites.remove(bullet)	#Roof
			if bullet.pos.y >= SCREEN_Y:	self.bullet_sprites.remove(bullet)	#Floor

	def generate_platforms(self):
		"""
		Generates platforms.
		"""
		for rocket in self.rockets:
			platform = Platform(rocket.uid, self.spritesheet)
			self.platforms.add(platform)

	def respawn_ships(self):
		"""
		Method to respawn rocket if destroyed.
		Will run on custom userevent to respawn a rocket that has been destroyed.
		"""
		if self.player1.invisible: self.player1.respawn()
		if self.player2.invisible: self.player2.respawn()
		
	def spawn_astroid(self):
		"""
		Spawn astroid if we havent reached the limit.
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
	Runs the game.
	Sets up the engine and starts the game loop.
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