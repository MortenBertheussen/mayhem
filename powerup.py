#!/usr/bin/env python3
from gameconstants import *
from Vector2D import *
from spritesheet import *
from movingobject import *
import random

class Powerup(Movingobject):
	def __init__(self, rect, spritesheet):
		super().__init__()
		self.pos = Vector2D(random.uniform(100,1100), random.uniform(100,700))
		self.spritesheet = spritesheet
		self.image = self.spritesheet.get_image((rect))
		self.image_pos = rect
		self.rect = self.image.get_rect()
		self.rect.centerx = self.pos.x
		self.rect.centery = self.pos.y