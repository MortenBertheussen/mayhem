#!/usr/bin/env python3
from gameconstants import *
from Vector2D import *
from spritesheet import *
from Movingobjects import *
import math

class Planet(Movingobject):
	def __init__(self, pos, rect):
		super().__init__()
		self.pos = Vector2D(pos[0], pos[1])
		self.spritesheet = Spritesheet("sprites/spritesheet.png")
		self.image = self.spritesheet.get_image((rect))
		self.image_pos = rect
		self.rect = self.image.get_rect()
		self.angle = 0
		self.rect.x = self.pos.x
		self.rect.y = self.pos.y

	def update(self):
		self.angle += 0.5
		self.new_sprite(self.image_pos)

	def new_sprite(self, rect):
		oldrect = self.rect
		self.image = self.spritesheet.get_image(rect)
		self.image = pygame.transform.rotate(self.image, self.angle)
		self.rect = self.image.get_rect(center=oldrect.center)