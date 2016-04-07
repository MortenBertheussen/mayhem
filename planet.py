#!/usr/bin/env python3
from gameconstants import *
from Vector2D import *
from spritesheet import *
from movingobject import *
import math

class Planet(Movingobject):
	"""The class for planet"""
	def __init__(self, pos, rect):
		super().__init__()
		self.pos = Vector2D(pos[0], pos[1])
		self.spritesheet = Spritesheet("sprites/spritesheet.png")
		self.image = self.spritesheet.get_image((rect))
		self.image_pos = rect
		self.rect = self.image.get_rect()
		self.angle = 0
		self.gravity = 10 
		self.rect.centerx = self.pos.x
		self.rect.centery = self.pos.y
		self.mass = 100

	def update(self):
		"""Runs what is needed for the class"""
		self.angle += 0.5
		self.new_sprite(self.image_pos)

	def new_sprite(self, rect):
		"""Fetches a new sprite from the spritesheet and keep its rotation"""
		oldrect = self.rect
		self.image = self.spritesheet.get_image(rect)
		self.image = pygame.transform.rotate(self.image, self.angle)
		self.rect = self.image.get_rect(center=oldrect.center)