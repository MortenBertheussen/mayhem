#!/usr/bin/env python3
from gameconstants import *
from Vector2D import *
from spritesheet import *
from staticobject import *
import math

class Planet(StaticObject):
	"""
	Creates a planet object.

	Planet(spawn, spriterect, spritesheet) -> object

	Parameters
	----------
	spawn : touple
		Initial spawn location.
	spritesheet : spritesheet object
		Pointer to spritesheet object.
	spriterect : (x,y,w,h)
		Position where image is located on spritesheet.
	"""
	def __init__(self, spawn, spriterect, spritesheet):
		super().__init__(spawn, spriterect, spritesheet)
		self.mass = PLANET_MASS

	def update(self):
		"""
		Update method for sprite group.

		update() -> none
		"""
		self.rect.center = (self.pos.x, self.pos.y)
		self.angle += 0.5
		self.rotate_image()