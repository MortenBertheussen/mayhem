#!/usr/bin/env python3
from gameconstants import *
from Vector2D import *
from spritesheet import *
from movingobject import *
import math

class Bullet(Movingobject):
	"""The bullet class"""
	def __init__(self, position, speed, angle, uid, wing):
		super().__init__()
		self.uid = uid
		self.speed = speed
		self.angle = angle
		if uid is 1:	self.spriterect = RED_LASER
		else:			self.spriterect = BLUE_LASER
		self.spritesheet = Spritesheet("sprites/spritesheet.png")
		self.image = self.spritesheet.get_image((self.spriterect))
		self.rect = self.image.get_rect()
		#self.pos.x = position.centerx
		#self.pos.y = position.centery
		self.center = Vector2D(position.centerx, position.centery)
		if wing is 1:
			point = Vector2D(position.centerx-15, position.centery-10)
			self.pos = self.rotate_point(point, self.center, angle)
		else:
			point = Vector2D(position.centerx+15, position.centery-10)
			self.pos = self.rotate_point(point, self.center, angle)
		print (position.centerx)
		print (position.centery)


		self.new_sprite(self.spriterect)

	def update(self):
		"""Runs what is needed for the class"""
		self.pos += self.speed.normalized() * 17
		self.rect.centerx = self.pos.x
		self.rect.centery = self.pos.y