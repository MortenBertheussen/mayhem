#!/usr/bin/env python3
from gameconstants import *
from Vector2D import *
import math

class Movingobject(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.gravity = Vector2D(0,1)
		self.maxspeed = 10
		self.pos = Vector2D(SCREEN_X/2 - 22, SCREEN_Y/2 - 22)
		self.direction = Vector2D(0,-1)

	def rotate(self):
		pass

class Rocket(Movingobject): 
	"""The class for rocket, broombroom"""
	def __init__(self):
		super().__init__()
		self.image = pygame.Surface([44, 59])
		self.image = pygame.image.load("sprites/ship.png").convert_alpha()
		self.rect = (self.pos.x, self.pos.y)
		self.engineOn = False
		self.turnLeft = False
		self.turnRight = False
		self.fuel = 100
		self.angle = 0


	def logic(self, screen):
		self.speed_limit()
		self.move()
		pygame.draw.rect(screen,RED,(self.pos.x,self.pos.y,45,45))

	def move(self):
		if self.turnLeft:
			self.angle += 4
		if self.turnRight:
			self.angle -= 4
		x = self.direction.x * math.cos(math.radians(-self.angle)) - self.direction.y * math.sin(math.radians(-self.angle))
		y = self.direction.x * math.sin(math.radians(-self.angle)) + self.direction.y * math.cos(math.radians(-self.angle))
		new_speed = Vector2D(x, y)

		if self.engineOn:
			self.image = pygame.image.load("sprites/ship_engine_on.png").convert_alpha()
			self.image = pygame.transform.rotate(self.image, self.angle)
			self.direction *= 1.3
			self.pos += new_speed + self.gravity
			self.rect = (self.pos.x, self.pos.y)
		else:
			self.image = pygame.image.load("sprites/ship.png").convert_alpha()
			self.image = pygame.transform.rotate(self.image, self.angle)
			self.direction /= 1.1
			self.pos += new_speed + self.gravity
			self.rect = (self.pos.x, self.pos.y)

	def speed_limit(self):
		if self.direction.magnitude() > self.maxspeed:
			self.direction = self.direction.normalized() * self.maxspeed

	def shoot(self):
		pass

	def refule(self):
		pass
		
