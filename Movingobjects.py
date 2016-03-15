#!/usr/bin/env python3

class Movingobject:
	def __init__(self):
		self.gravity = Vector2D(0,9)

	def rotate(self):
		pass

class Rocket(Movingobject): 
	"""The class for rocket, broombroom"""
	def __init__(self):
		super().__init__(self)
		self.pos = Vector2D(0,0)
		self.speed = Vector2D(0,0)
		self.engineOn = False

	def draw(self):
		"""Draw the rocket in its current possition."""
		pygame.draw.rect(screen, (150,0,0), (self.possition.x, self.pos.y, self.witdh, self.height), 0)

	def move(self):
		if engineOn:
			self.pos += self.speed + self.gravity
		else:
			self.pos += self.gravity
