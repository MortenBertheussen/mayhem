#!/usr/bin/env python3
from gameconstants import *
from Vector2D import *
from spritesheet import *
from staticobject import *
import math

class Planet(StaticObject):
	"""The class for planet"""
	def __init__(self, spawn, spriterect, spritesheet):
		super().__init__(spawn, spriterect, spritesheet)
		self.mass = PLANET_MASS

	def update(self):
		"""Runs what is needed for the class"""
		self.rect.center = (self.pos.x, self.pos.y)
		self.angle += 0.5
		self.rotate_image()