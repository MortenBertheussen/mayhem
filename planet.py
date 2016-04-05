#!/usr/bin/env python3
from gameconstants import *
from Vector2D import *
from spritesheet import *
from Movingobject import *
import math

class Planet(Movingobject):
	def __init__(self, pos, grav):
		super().__init__()
		self.pos = Vector2D(pos[0], pos[1])
		self.gravity = grav
		self.image = None
		self.rect = self.image.get_rect()