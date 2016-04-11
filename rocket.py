#!/usr/bin/env python3
from gameconstants import *
from Vector2D import *
from spritesheet import *
from movingobject import *
from bullet import *
import math

class Rocket(Movingobject): 
	"""The class for rocket"""
	def __init__(self, uid, spritesheet):
		super().__init__()
		self.uid = uid
		self.spritesheet = spritesheet
		self.image = self.spritesheet.get_image((0,0,30,30))
		self.rect = self.image.get_rect()
		self.engineOn = False
		self.turnLeft = False
		self.turnRight = False
		self.dead = False
		self.refuel = False
		self.fuel = 1000
		self.health = 100
		self.maxhealth = 200
		self.maxfuel = 1000
		self.invisible = False
		self.speedBreak = False
		self.score = 0
		self.mass = 5
		if self.uid == 1:
			self.spawn = Vector2D(150,SCREEN_Y-145) #Calc this from the players platform later, no magic numbers
			self.pos = self.spawn
		elif self.uid == 2:
			self.spawn = Vector2D(SCREEN_X-150, 155) #Calc this from the players platform later, no magic numbers
			self.pos = self.spawn

	def update(self):
		"""Runs what is needed for the class"""

		if self.dead:
			self.despawn()
		else:
			#print("Doing stuff")
			self.current_sprite()
			self.speed_limit()
			self.move()
			self.screen_wrap()
			if self.refuel:
				self.fuel_up()

	def current_sprite(self):
		"""Set image to right sprite from the spritesheet"""
		if self.invisible:
			return
		if self.uid is 1:
			#ENGINE ON SPRITES (PLAYER1)
			if self.engineOn:
				if self.health is 75:	self.new_sprite(RED_ENGINE_ON_75)
				elif self.health is 50:	self.new_sprite(RED_ENGINE_ON_50)
				elif self.health is 25:	self.new_sprite(RED_ENGINE_ON_25)
				else:					self.new_sprite(RED_ENGINE_ON)
			#ENGINE OFF SPRITES (PLAYER1)
			else:
				if self.health is 75:	self.new_sprite(RED_ENGINE_OFF_75)
				elif self.health is 50:	self.new_sprite(RED_ENGINE_OFF_50)
				elif self.health is 25:	self.new_sprite(RED_ENGINE_OFF_25)
				else:					self.new_sprite(RED_ENGINE_OFF)

		else:
			#ENGINE ON SPRITES (PLAYER2)
			if self.engineOn:
				if self.health is 75:	self.new_sprite(BLUE_ENGINE_ON_75)
				elif self.health is 50:	self.new_sprite(BLUE_ENGINE_ON_50)
				elif self.health is 25:	self.new_sprite(BLUE_ENGINE_ON_25)
				else:					self.new_sprite(BLUE_ENGINE_ON)
			#ENGINE OFF SPRITES (PLAYER2)
			else:
				if self.health is 75:	self.new_sprite(BLUE_ENGINE_OFF_75)
				elif self.health is 50:	self.new_sprite(BLUE_ENGINE_OFF_50)
				elif self.health is 25:	self.new_sprite(BLUE_ENGINE_OFF_25)
				else:					self.new_sprite(BLUE_ENGINE_OFF)

	def move(self):
		"""Move method of rocket"""
		if self.turnLeft: self.rotate_left()
		if self.turnRight: self.rotate_right()

		if self.speedBreak and self.speed.magnitude() > 1:
			self.speed /= 1.04

		#ENGINE ON
		if self.engineOn and self.fuel>0:
			self.speed *= 1.25
			self.pos += self.speed
			self.rect.center = (self.pos.x, self.pos.y)
			self.refuel = False
			self.fuel -=1
			
			if self.fuel <= 0: self.fuel = 0	#Set fuel not to go under 0

		#ENGINE OFF
		else:
			if self.speed.magnitude() > 1:
				#self.speed /= 1.04
				self.pos += self.speed
			self.rect.center = (self.pos.x, self.pos.y)

	def shoot(self, wing):
		"""Shoot method of rocket"""
		#Create a bullet object with the ships position and user id
		return Bullet(self.rect, self.speed, self.angle, self.uid, wing)


	def bullet_impact(self):
		"""Method when ship is hit by a bullet"""
		self.health -= 25
	
	def despawn(self):
		self.invisible = True
		self.dead = False
		self.speed = Vector2D(0,-1)
		self.pos = self.spawn
		self.health = 0

		self.new_sprite(BLANK_SPRITE)
		pygame.time.set_timer(RESPAWN_TIMER, 1500)

	def respawn(self):
		"""Method to respawn the ship.
		Used when coliding with the environment or when health is 0"""
		self.pos = self.spawn
		self.fuel = 1000
		self.angle = 0
		self.health = 100
		self.speed = Vector2D(0,-1)
		self.invisible = False

	def fuel_up(self):
		"""fuel method"""
		if self.fuel > self.maxfuel:
			self.fuel = self.maxfuel
		if self.refuel and self.fuel < self.maxfuel:
			self.fuel += 5