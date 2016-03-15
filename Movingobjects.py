#!/usr/bin/env python3
from gameconstants import *
from Vector2D import *

class Movingobject:
	def __init__(self):
		self.gravity = Vector2D(0,10)
		self.maxspeed = 30
		self.pos = Vector2D(SCREEN_X/2, SCREEN_Y/2)
		self.direction = Vector2D(0,-1)

	def rotate(self):
		pass

class Rocket(Movingobject): 
	"""The class for rocket, broombroom"""
	def __init__(self):
		super().__init__()
		self.witdh = 20
		self.height = 40
		self.engineOn = False
		self.fule = 100

	def logic(self, screen):
		self.speed_limit()
		self.move()
		self.draw(screen)

	def draw(self, screen):
		"""Draw the rocket in its current possition."""
		pygame.draw.rect(screen, (150,0,0), (self.pos.x, self.pos.y, self.witdh, self.height), 0)

	def move(self):
		if self.engineOn:
			self.direction *= 1.3
			self.pos += self.direction + self.gravity
		else:
			self.direction /= 1.1
			self.pos += self.direction + self.gravity

	def speed_limit(self):
		if self.direction.magnitude() > self.maxspeed:
			self.direction = self.direction.normalized() * self.maxspeed

	def shoot(self):
		pass

	def refule(self):
		pass
		
