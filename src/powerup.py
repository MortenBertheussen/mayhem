#!/usr/bin/env python3
from gameconstants import *
from Vector2D import *
from spritesheet import *
from staticobject import *
import random

class PowerUp(StaticObject):
	def __init__(self, powertype, spawn, spriterect, spritesheet):
		super().__init__(spawn, spriterect, spritesheet)
		self.type = powertype
		self.resize_image(20,20)

	def update(self):
		self.rect.center = (self.pos.x, self.pos.y)