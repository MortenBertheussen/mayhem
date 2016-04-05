#!/usr/bin/env python3
from gameconstants import *
from Vector2D import *
from spritesheet import *
import math

class Movingobject(pygame.sprite.Sprite):
	"""A class for movingobjects"""
	def __init__(self):
		super().__init__()
		self.maxspeed = 5
		self.pos = Vector2D(SCREEN_X/2 - 22, SCREEN_Y/2 - 22)
		self.direction = Vector2D(0,-1)

	def screen_wrap(self):
		"""Make moving objects wrap around if they go out of the screen"""
		#Left
		if self.pos.x <= 0:
			self.pos.x = SCREEN_X - 1
		#Right
		if self.pos.x >= SCREEN_X:
			self.pos.x = 1
		#Bottom
		if self.pos.y >= SCREEN_Y:
			self.pos.y = 1
		#Top
		if self.pos.y <= 0:
			self.pos.y = SCREEN_Y - 1 

	def rotate(self):
		"""The math behind finding the new direction with an angle"""
		x = self.direction.x * math.cos(math.radians(-self.angle)) - self.direction.y * math.sin(math.radians(-self.angle))
		y = self.direction.x * math.sin(math.radians(-self.angle)) + self.direction.y * math.cos(math.radians(-self.angle))
		new_speed = Vector2D(x, y)

		return new_speed

	def new_sprite(self, rect):
		oldrect = self.rect
		self.image = self.spritesheet.get_image(rect)
		self.image = pygame.transform.rotate(self.image, self.angle)
		self.rect = self.image.get_rect(center=oldrect.center)


	def update_sprite(self, img):
		"""updates the sprites"""
		oldrect = self.rect
		self.image = pygame.image.load(img).convert_alpha()
		self.image = pygame.transform.scale(self.image,(35,35))
		self.image = pygame.transform.rotate(self.image, self.angle)
		self.rect = self.image.get_rect(center=oldrect.center) # Reposition sprite to its center

class Rocket(Movingobject): 
	"""The class for rocket, broombroom"""
	def __init__(self, uid):
		super().__init__()
		self.uid = uid
		self.spritesheet = Spritesheet("sprites/spritesheet.png")
		self.image = self.spritesheet.get_image((0,0,30,30))
		self.rect = self.image.get_rect()
		self.engineOn = False
		self.turnLeft = False
		self.turnRight = False
		self.refuel = False
		self.fuel = 1000
		self.health = 100
		self.maxfuel = 1000
		self.score = 0
		self.angle = 0
		self.shots = []
		if self.uid == 1:
			self.spawn = Vector2D(150,SCREEN_Y-120) #Calc this from the players platform later, no magic numbers
			self.pos = self.spawn
		elif self.uid == 2:
			self.spawn = Vector2D(SCREEN_X-150, 180) #Calc this from the players platform later, no magic numbers
			self.pos = self.spawn

	def update(self):
		self.current_sprite()
		self.speed_limit()
		self.angle_fix()
		self.move()
		self.screen_wrap()
		if self.refuel:
			self.fule()

	def angle_fix(self):
		"""Keeps the angle between 0 and 360 degrees. We dont want negative angles."""
		self.angle = self.angle % 360

	def current_sprite(self):
		if self.uid is 1:
			if self.engineOn:
				if self.health is 75:
					self.new_sprite(RED_ENGINE_ON_75)
				elif self.health is 50:
					self.new_sprite(RED_ENGINE_ON_50)
				elif self.health is 25:
					self.new_sprite(RED_ENGINE_ON_25)
				else:
					self.new_sprite(RED_ENGINE_ON)
				
			else:
				if self.health is 75:
					self.new_sprite(RED_ENGINE_OFF_75)
				elif self.health is 50:
					self.new_sprite(RED_ENGINE_OFF_50)
				elif self.health is 25:
					self.new_sprite(RED_ENGINE_OFF_25)
				else:
					self.new_sprite(RED_ENGINE_OFF)

		else:
			if self.engineOn:
				if self.health is 75:
					self.new_sprite(BLUE_ENGINE_ON_75)
				elif self.health is 50:
					self.new_sprite(BLUE_ENGINE_ON_50)
				elif self.health is 25:
					self.new_sprite(BLUE_ENGINE_ON_25)
				else:
					self.new_sprite(BLUE_ENGINE_ON)
			else:
				if self.health is 75:
					self.new_sprite(BLUE_ENGINE_OFF_75)
				elif self.health is 50:
					self.new_sprite(BLUE_ENGINE_OFF_50)
				elif self.health is 25:
					self.new_sprite(BLUE_ENGINE_OFF_25)
				else:
					self.new_sprite(BLUE_ENGINE_OFF)

	def move(self):
		"""Move method of rocket"""
		if self.turnLeft: self.angle += 3
		if self.turnRight: self.angle -= 3
		
		new_speed = self.rotate()

		#ENGINE ON
		if self.engineOn and self.fuel>0:
			self.direction *= 1.5
			self.pos += new_speed
			self.rect.center = (self.pos.x, self.pos.y)
			self.refuel = False
			self.fuel -=1
			
			if self.fuel <= 0: self.fuel = 0	#Set fuel not to go under 0

		#ENGINE OFF
		else:
			if self.direction.magnitude() > 0.01:
				self.direction /= 1.04
				self.pos += new_speed
			self.rect.center = (self.pos.x, self.pos.y)

	def speed_limit(self):
		"""Speed_limit method of rocket"""
		if self.direction.magnitude() > self.maxspeed:
			self.direction = self.direction.normalized() * self.maxspeed

	def shoot(self):
		"""Shoot method of rocket"""
		#Create a bullet object with the ships position and user id
		return Bullet(self.rect, self.rotate(), self.angle, self.uid)

	def bullet_impact(self):
		"""Method when ship is hit by a bullet"""
		self.health -= 25

	def respawn(self):
		"""Method to respawn the ship.
		Used when coliding with the environment or when health is 0"""
		self.pos = self.spawn
		self.fuel = 1000
		self.angle = 0
		self.health = 100
		self.direction = self.direction.normalized()

	def fule(self):
		"""fuel method"""
		if self.fuel > self.maxfuel:
			self.fuel = self.maxfuel
		if self.refuel and self.fuel < self.maxfuel:
			self.fuel += 5

class Bullet(Movingobject):
	"""The bullet class"""
	def __init__(self, rect, direc, angle, uid):
		super().__init__()
		self.uid = uid
		self.dir = direc
		self.angle = angle
		if uid is 1:
			self.spriterect = RED_LASER
		else:
			self.spriterect = BLUE_LASER
		self.spritesheet = Spritesheet("sprites/spritesheet.png")
		self.image = self.spritesheet.get_image((self.spriterect))
		self.rect = self.image.get_rect()
		self.pos.x = rect.center[0]
		self.pos.y = rect.center[1]

		self.new_sprite(self.spriterect)

	def move(self):
		"""Moves the bullet"""
		self.pos += self.dir.normalized() * 15
		self.rect.x = self.pos.x
		self.rect.y = self.pos.y

	def update(self):
		self.move()

