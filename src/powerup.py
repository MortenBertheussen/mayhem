#!/usr/bin/env python3
from gameconstants import *
from Vector2D import *
from spritesheet import *
from staticobject import *
import random

class PowerUp(StaticObject):
	"""
	Creates a powerup object.

	Bullet(powertype, spawn, spriterect, spritesheet) -> object

	Parameters
	----------
	powertype : string, "hp" or "shield" or "missile"
		Type of powerup.
	spawn : touple
		Initial spawn position.
	spriterect : (x,y,w,h)
		Position on spritesheet to get image.
	spritesheet : spritesheet object
		Pointer to spritesheet object.
	"""
	def __init__(self, powertype, spawn, spriterect, spritesheet):
		super().__init__(spawn, spriterect, spritesheet)
		self.type = powertype
		self.resize_image(20,20)

	def update(self):
		"""
		Update method for sprite group.

		update() -> none
		"""
		self.rect.center = (self.pos.x, self.pos.y)