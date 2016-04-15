#!/usr/bin/env python3
from gameconstants import *
from config import *
from Vector2D import *
from spritesheet import *
from movingobject import *
from bullet import *
import math

class Rocket(Movingobject): 
	"""
	Creates a rocket object.

	Rocket(uid, spritesheet, sprite_rect, spawn) -> object

	Parameters
	----------
	uid : int
		Identified for who shot the bullet.
	spritesheet : spritesheet object
		Pointer to spritesheet object.
	sprite_rect : (x,y,w,h)
		Position on spritesheet to get image.
	spawn : touple
		Initial spawn position.
	"""

	def __init__(self, uid, spritesheet, sprite_rect, spawn):
		super().__init__(uid, spritesheet, spawn)
		self.image = self.spritesheet.get_image(sprite_rect)
		self.rect = self.image.get_rect()
		self.engineOn = False
		self.turnLeft = False
		self.turnRight = False
		self.dead = False
		self.refuel = False
		self.invisible = False
		self.speedBreak = False
		self.shield = False
		self.fuel = STARTING_FUEL
		self.maxfuel = MAX_FUEL
		self.health = STARTING_HP
		self.score = 0
		self.mass = PLAYER_MASS
		self.missiles = 0

	def update(self):
		"""
		Update method for sprite group.

		update() -> none
		"""
		if self.dead:
			self.despawn()
		else:
			self.current_sprite()
			self.speed_limit()
			self.move()
			self.screen_wrap()
			if self.refuel:
				self.fuel_up()

	def current_sprite(self):
		"""
		Set image to correct sprite for the current state of the rocket from the spritesheet.

		current_sprite() -> none
		"""
		if self.invisible:
			return
		if self.uid is 1:
			#ENGINE ON SPRITES (PLAYER1)
			if self.engineOn:
				if self.shield:		self.new_sprite(RED_ENGINE_ON_SHIELD)
				else:				self.new_sprite(RED_ENGINE_ON)
			#ENGINE OFF SPRITES (PLAYER1)
			else:
				if self.shield:		self.new_sprite(RED_ENGINE_OFF_SHIELD)
				else:				self.new_sprite(RED_ENGINE_OFF)

		else:
			#ENGINE ON SPRITES (PLAYER2)
			if self.engineOn:
				if self.shield:		self.new_sprite(BLUE_ENGINE_ON_SHIELD)
				else:				self.new_sprite(BLUE_ENGINE_ON)
			#ENGINE OFF SPRITES (PLAYER2)
			else:
				if self.shield:		self.new_sprite(BLUE_ENGINE_OFF_SHIELD)
				else:				self.new_sprite(BLUE_ENGINE_OFF)

	def move(self):
		"""
		Moves the rocket.

		move() -> none
		"""
		if self.fuel <= 0: self.fuel = 0	#Set fuel not to go under 0

		#ENGINE ON
		if self.engineOn and self.fuel>0:
			self.speed *= 1.25
			self.refuel = False
			self.fuel -=1

		#Turning
		if self.turnLeft: self.rotate(-4)
		if self.turnRight: self.rotate(4)

		#Break
		if self.speedBreak and self.speed.magnitude() > 1:
			self.speed /= 1.04

		#Movement
		if self.speed.magnitude() > 1:	#Only move with speed if speed is big enough
			self.pos += self.speed
		self.rect.center = (self.pos.x, self.pos.y)

	def shoot(self, wing):
		"""
		Rocket fires.

		shoot(wing) -> object

		Parameters:
		-----------
		wing: string, "left" or "right"
			What wing the bullet should spawn on.
		"""
		#Create a bullet object with the ships position and user id
		if self.missiles > 0:
			self.missiles -= 1
			return Missile(self.uid, self.spritesheet, (self.pos.x, self.pos.y), self.speed, self.angle, wing)
		else:
			return Bullet(self.uid, self.spritesheet, (self.pos.x, self.pos.y), self.speed, self.angle, wing)

	def rotate(self, angle):
		"""
		Rotate the speed vector by an angle.
		rotate(angle) -> none

		Parameters:
		-----------
		angle: int
		"""
		rad = math.radians(angle)
		x = self.speed.x * math.cos(rad) - self.speed.y * math.sin(rad)
		y = self.speed.x * math.sin(rad) + self.speed.y * math.cos(rad)
		self.speed = Vector2D(x, y)
		self.calc_angle()

	def shield_down(self):
		"""
		Disables the shield on the rocket and stops timer.
		
		shield_down() -> none
		"""
		self.shield = False
		if self.uid is 1: pygame.time.set_timer(SHIELD_PLAYER1, 0)	#Stop timer
		if self.uid is 2: pygame.time.set_timer(SHIELD_PLAYER2, 0)	#Stop timer

	def shield_up(self):
		"""
		Enbles the shield on the rocket and starts timer.
		
		shield_up() -> none
		"""
		self.shield = True
		if self.uid is 1: pygame.time.set_timer(SHIELD_PLAYER1, SHIELD_DURATION)	#Start timer
		if self.uid is 2: pygame.time.set_timer(SHIELD_PLAYER2, SHIELD_DURATION)	#Start timer
	
	def despawn(self):
		"""
		Despawns rocket.
		
		despawn() -> none
		"""
		self.invisible = True 								#Set rocket to invisible
		self.dead = False									#No longer dead
		self.speed = Vector2D(0,-1)							#Reset speed vector
		self.pos = Vector2D(self.spawn[0], self.spawn[1])	#Reset positon
		self.health = 0										#Health 0 when dead
		self.fuel = 0										#Fuel 0 when dead
		self.shield = False									#Disable shield
		self.missiles = 0									#Reset missiles
		self.angle = 0										#Reset angle

		self.new_sprite(BLANK_SPRITE)						#Sprite is blank, no collision
		if self.uid is 1: pygame.time.set_timer(RESPAWN_PLAYER1, 1500)	#Start timer
		if self.uid is 2: pygame.time.set_timer(RESPAWN_PLAYER2, 1500)	#Start timer

	def respawn(self):
		"""
		Respawns rocket.
		
		respawn() -> none
		"""
		self.invisible = False
		if self.uid is 1: pygame.time.set_timer(RESPAWN_PLAYER1, 0)	#Stop timer
		if self.uid is 2: pygame.time.set_timer(RESPAWN_PLAYER2, 0)	#Stop timer

	def fuel_up(self):
		"""
		Increase fuel on rocket.
		
		fuel_up() -> none
		"""
		if self.fuel > self.maxfuel:	#Dont allow over maxfuel
			self.fuel = self.maxfuel
		if self.refuel and self.fuel < self.maxfuel and self.invisible is False:
			self.fuel += 5 #Refueling