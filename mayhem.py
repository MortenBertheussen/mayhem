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
		self.powerup = pygame.sprite.Group()		#Powerup sprites
		self.planets = pygame.sprite.Group()		#Planet sprites
		self.astroids = pygame.sprite.Group()		#Astroid sprites
		self.spritesheet = Spritesheet("sprites/spritesheet.png")

		self.generate_player()						#Generate all players
		self.generate_planets()						#Genereate all planets
		self.spawn_powerups()						#Generate powerup
		self.bg.add(Background())					#Add background
		self.hud.add(Hud())							#Add hud

	def logic(self, screen):
		"""
		Logic method that runs all the engines methods needed for each frame.
		Takes in a screen as a parameter to draw the game.
		Engine.login(screen)
		"""
		self.eventhandler()

		#Update all spritegroups
		self.bg.update()
		self.hud.update()
		self.explotions.update()
		self.rockets.update()
		self.bullet_sprites.update()
		self.platforms.update()
		self.planets.update()
		self.astroids.update()
		self.powerup.update()

		#Collision detection and misc methods
		self.gravity_field()
		self.bullet_impact()
		self.environment_impact()
		self.bullet_out_of_screen()

		#Drawing
		self.bg.draw(screen)				#Draw background sprite
		self.platforms.draw(screen)			#Draw platform sprites
		self.bullet_sprites.draw(screen)	#Draw bullet sprites
		self.powerup.draw(screen)			#Draw powerup sprites
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

	def respawn_ships(self):
		"""
		Method to respawn rocket if destroyed.
		Will run on custom userevent to respawn a rocket that has been destroyed.
		"""
		for rocket in self.rockets:
			if rocket.invisible:
				rocket.respawn()

	def eventhandler(self):
		"""
		Handles all user input and custom userevents.
		"""
		for event in pygame.event.get():
			if event.type == pygame.QUIT: exit()					#Exit when clicking to close window			if event.type == ASTROID_SPAWN: self.spawn_astroid()	#EVENT FOR SPAWNING NEW ASTROIDS
			if event.type == RESPAWN_TIMER: self.respawn_ships()	#Event for respawning dead ships
			if event.type == ASTROID_SPAWN: self.spawn_astroid()	#Event for respawning dead ships
			if event.type == pygame.KEYDOWN:
				for rocket in self.rockets:
					#Player 1
					if rocket.uid == 1:
						if rocket.invisible is False:
							if event.key == pygame.K_w:	rocket.engineOn = True
							if event.key == pygame.K_a: rocket.turnLeft = True
							if event.key == pygame.K_d: rocket.turnRight = True
							if event.key == pygame.K_s: rocket.speedBreak = True
							if event.key == pygame.K_SPACE:
								bullet1 = Bullet(rocket.rect, rocket.speed, rocket.angle, rocket.uid, 1, self.spritesheet)
								bullet2 = Bullet(rocket.rect, rocket.speed, rocket.angle, rocket.uid, 2, self.spritesheet)
								self.bullet_sprites.add(bullet1)
								self.bullet_sprites.add(bullet2)
					#Player 2
					if rocket.uid == 2:
						if rocket.invisible is False:
							if event.key == pygame.K_UP:	rocket.engineOn = True
							if event.key == pygame.K_LEFT:	rocket.turnLeft = True
							if event.key == pygame.K_RIGHT:	rocket.turnRight = True
							if event.key == pygame.K_DOWN: rocket.speedBreak = True
							if event.key == pygame.K_PERIOD:
								bullet1 = Bullet(rocket.rect, rocket.speed, rocket.angle, rocket.uid, 1, self.spritesheet)
								bullet2 = Bullet(rocket.rect, rocket.speed, rocket.angle, rocket.uid, 2, self.spritesheet)
								self.bullet_sprites.add(bullet1)
								self.bullet_sprites.add(bullet2)

			if event.type == pygame.KEYUP:
				for rocket in self.rockets:
					#Player 1
					if rocket.uid == 1:
						if event.key == pygame.K_w: rocket.engineOn = False
						if event.key == pygame.K_a: rocket.turnLeft = False
						if event.key == pygame.K_d: rocket.turnRight = False
						if event.key == pygame.K_s: rocket.speedBreak = False

					#Player 2
					if rocket.uid == 2:
						if event.key == pygame.K_UP: rocket.engineOn = False
						if event.key == pygame.K_LEFT: rocket.turnLeft = False
						if event.key == pygame.K_RIGHT: rocket.turnRight = False
						if event.key == pygame.K_DOWN: rocket.speedBreak = False

	def gravity_force(self, object1, object2):
		"""
		Calculates the strenght of gravity between two objects.
		A simplified version of Newton's Law of Universal Gravitation.
		"""
		distance = (object1.pos - object2.pos).magnitude()
		f = (object1.mass * object2.mass) / (distance ** 2)
		return f

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

		#Rocket
		for rocket in self.rockets:
			collide_rocket = pygame.sprite.spritecollide(rocket,self.bullet_sprites,False)
			
			for bullet in collide_rocket:
				if bullet.uid != rocket.uid and pygame.sprite.collide_mask(rocket, bullet):
					rocket.bullet_impact()	#Reduce health of rocket
					self.explotions.add( Explotion(bullet.rect.centerx, bullet.rect.centery, 30) )
					if rocket.health <= 0:
						self.explotions.add( Explotion(rocket.rect.centerx, rocket.rect.centery, 75) )
						rocket.dead = True
						for rocket in self.rockets:
							if rocket.uid is bullet.uid:
								rocket.score += 100 #Give the player who got the hit score
					self.bullet_sprites.remove(bullet)
		
		#Astroid
		for astroid in self.astroids:
			for bullet in self.bullet_sprites:
				hit = pygame.sprite.collide_rect(astroid, bullet)
				if hit and pygame.sprite.collide_mask(astroid, bullet):
					astroid.life -=1
					self.explotions.add( Explotion(bullet.rect.centerx, bullet.rect.centery, 20) )
					self.bullet_sprites.remove(bullet)
					if astroid.life == 0:
						for rocket in self.rockets:
							if rocket.uid is bullet.uid:
								rocket.score += 10
						self.explotions.add( Explotion(astroid.rect.centerx, astroid.rect.centery, 75) )
						self.astroids.remove(astroid)


		#Planet
		for planet in self.planets:
			for bullet in self.bullet_sprites:
				hit = pygame.sprite.collide_rect(planet, bullet)
				if hit and pygame.sprite.collide_mask(planet, bullet):
					self.explotions.add( Explotion(bullet.rect.centerx, bullet.rect.centery, 20) )
					self.bullet_sprites.remove(bullet)

		#Platform
		for platform in self.platforms:
			for bullet in self.bullet_sprites:
				hit = pygame.sprite.collide_rect(platform, bullet)
				if hit and bullet.uid != platform.uid and pygame.sprite.collide_mask(platform, bullet):
					self.explotions.add( Explotion(bullet.rect.centerx, bullet.rect.centery, 20) )
					self.bullet_sprites.remove(bullet)

	def environment_impact(self):
		"""
		Colision detection between astroids, planets, ships and platforms.
		"""
		for astroid in self.astroids:
			#Astroid -> Planet
			for planet in self.planets:
				hit = pygame.sprite.collide_rect(astroid, planet)
				if hit and pygame.sprite.collide_mask(astroid, planet):
					explotion = Explotion(astroid.rect.centerx, astroid.rect.centery, 30)
					self.explotions.add(explotion)
					self.astroids.remove(astroid)
			#Astroid -> Ship
			for rocket in self.rockets:
				hit = pygame.sprite.collide_rect(astroid, rocket)
				if hit and pygame.sprite.collide_mask(astroid, rocket):
					explotion = Explotion(rocket.rect.centerx, rocket.rect.centery, 30)
					self.explotions.add(explotion)
					rocket.score -= 10
					rocket.dead = True
			#Astroid -> Astroid
			for astroid2 in self.astroids:
				hit = pygame.sprite.collide_rect(astroid, astroid2)
				if hit and (astroid != astroid2) and (SCREEN_X -50 > astroid.rect.x > 50) and ( SCREEN_Y - 50 > astroid.rect.y > 50) and pygame.sprite.collide_mask(astroid, astroid2):
					if astroid.type is 1:
						explotion = Explotion(astroid.rect.centerx, astroid.rect.centery, 60)
					elif astroid.type is 2:
						explotion = Explotion(astroid.rect.centerx, astroid.rect.centery, 40)
					else:
						explotion = Explotion(astroid.rect.centerx, astroid.rect.centery, 30)
					explotion2 = Explotion(astroid2.rect.centerx, astroid2.rect.centery, 30)
					self.explotions.add(explotion)
					self.explotions.add(explotion2)
					if astroid.type != astroid2.type:
						#Collision between big astroid and smaller
						if astroid.type is 1:
							if astroid2.type is 2:
								new_astroid = Astroid( (astroid.pos.x-20, astroid.pos.y), ASTROID_2, self.spritesheet, astroid.speed*0.7)
								new_astroid2 = Astroid( (astroid.pos.x+20, astroid.pos.y), ASTROID_2, self.spritesheet, astroid.speed*0.7*-1)
								self.astroids.remove(astroid2)
								self.astroids.remove(astroid)
								self.astroids.add(new_astroid)
								self.astroids.add(new_astroid2)
							if astroid2.type is 3:
								astroid.speed *= ENERGY_LOSS_SMALL
								self.astroids.remove(astroid2)

						if astroid.type is 2 and astroid2.type is 3:
							new_astroid = Astroid( (astroid.pos.x-20, astroid.pos.y), ASTROID_3, self.spritesheet, astroid.speed*ENERGY_LOSS)
							new_astroid2 = Astroid( (astroid.pos.x+20, astroid.pos.y), ASTROID_3, self.spritesheet, astroid.speed*ENERGY_LOSS*-1)
							self.astroids.remove(astroid)
							self.astroids.remove(astroid2)
							self.astroids.add(new_astroid)
							self.astroids.add(new_astroid2)

					else:
						if astroid.type is 1:
							new_astroid1 = Astroid( (astroid.pos.x-20, astroid.pos.y), ASTROID_2, self.spritesheet, astroid.speed*ENERGY_LOSS )
							new_astroid2 = Astroid( (astroid.pos.x+20, astroid.pos.y), ASTROID_2, self.spritesheet, astroid.speed*ENERGY_LOSS*-1 )
							self.astroids.add(new_astroid1)
							self.astroids.add(new_astroid2)
						elif astroid.type is 2:
							new_astroid1 = Astroid( (astroid.pos.x-20, astroid.pos.y), ASTROID_3, self.spritesheet, astroid.speed*ENERGY_LOSS)
							new_astroid2 = Astroid( (astroid.pos.x+20, astroid.pos.y), ASTROID_3, self.spritesheet, astroid.speed*ENERGY_LOSS*-1)
							self.astroids.add(new_astroid1)
							self.astroids.add(new_astroid2)

						self.astroids.remove(astroid)
						self.astroids.remove(astroid2)
					
			#Astroid -> Platform
			for platform in self.platforms:
				hit = pygame.sprite.collide_rect(astroid, platform)
				if hit and pygame.sprite.collide_mask(astroid, platform):
					explotion = Explotion(astroid.rect.centerx, astroid.rect.centery, 30)
					self.explotions.add(explotion)
					self.astroids.remove(astroid)

		for rocket in self.rockets:
			#Ship -> Planet
			for planet in self.planets:
				hit = pygame.sprite.collide_rect(rocket, planet)
				if hit and pygame.sprite.collide_mask(rocket, planet):
					explotion = Explotion(rocket.rect.centerx, rocket.rect.centery, 30)
					self.explotions.add(explotion)
					rocket.score -= 20
					rocket.dead = True
			#Ship -> Platform
			for platform in self.platforms:
				hit = pygame.sprite.collide_rect(rocket, platform)
				if hit and (platform.uid == rocket.uid):
					rocket.refuel = True
			#Ship -> Ship 
			for rocket2 in self.rockets:
				if rocket != rocket2:
					hit = pygame.sprite.collide_rect(rocket, rocket2)
					if hit and pygame.sprite.collide_mask(rocket,rocket2):
						explotion1 = Explotion(rocket.rect.centerx, rocket.rect.centery, 50)
						explotion2 = Explotion(rocket2.rect.centerx, rocket2.rect.centery, 50)
						self.explotions.add(explotion1)
						self.explotions.add(explotion2)
						rocket.dead = True
						rocket2.dead = True

	def bullet_out_of_screen(self):
		"""
		Removed bullets if they exit the screen.
		"""
		for bullet in self.bullet_sprites:
			if bullet.pos.x <= 0:			self.bullet_sprites.remove(bullet)	#Left wall
			if bullet.pos.x >= SCREEN_X:	self.bullet_sprites.remove(bullet)	#Right wall
			if bullet.pos.y <= 0:			self.bullet_sprites.remove(bullet)	#Roof
			if bullet.pos.y >= SCREEN_Y:	self.bullet_sprites.remove(bullet)	#Floor

	def generate_player(self):
		"""
		Generates players and their platform.
		"""
		#Generate ships with id
		for i in range(1,self.players+1):
			rocket = Rocket(i, self.spritesheet)
			self.rockets.add(rocket)

		#Generate platform for players with id
		for i in range(1,self.players+1):
			platform = Platform(i, self.spritesheet)
			self.platforms.add(platform)

	def generate_planets(self):
		"""
		Generate planets for the map.
		"""
		self.planets.add(Planet((SCREEN_X/2,SCREEN_Y/2),BLACK_HOLE,self.spritesheet))
		
	def spawn_astroid(self):
		"""
		Spawn astroid if we havent reached the limit.
		"""
		if len(self.astroids) < 10:
			astroid = Astroid(	ASTROID_SPAWNS[random.randint(0,7)],
								random.choice([ASTROID_1, ASTROID_2, ASTROID_3]),
								self.spritesheet  )
			self.astroids.add(astroid)
	def spawn_powerups(self):
		self.powerup.add(Powerup(SHIELD_BUFF, self.spritesheet))


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

	pygame.time.set_timer(ASTROID_SPAWN, 500) #Set a timer for spawning astroids

	while True:	
		clock.tick(FPS)
		engine.logic(screen)

if __name__ == "__main__":
	main()