#!/usr/bin/env python3
from gameconstants import *
from Vector2D import *
from spritesheet import *
from movingobject import *
import math

class Bullet(Movingobject):
	"""The bullet class"""
	def __init__(self, position, speed, angle, uid, wing, spritesheet):
		super().__init__()
		self.uid = uid
		self.type = "bullet"
		self.speed = speed
		self.angle = angle
		if uid is 1:	self.spriterect = RED_LASER
		else:			self.spriterect = BLUE_LASER
		self.spritesheet = spritesheet
		self.image = self.spritesheet.get_image((self.spriterect))
		self.rect = self.image.get_rect()
		#self.pos.x = position.centerx
		#self.pos.y = position.centery
		self.center = Vector2D(position.centerx, position.centery)
		if wing is 1:
			point = Vector2D(position.centerx-7, position.centery-10)
			self.pos = self.rotate_point(point, self.center, angle)
		else:
			point = Vector2D(position.centerx+7, position.centery-10)
			self.pos = self.rotate_point(point, self.center, angle)

		self.new_sprite(self.spriterect)

	def update(self):
		"""Runs what is needed for the class"""
		self.pos += self.speed.normalized() * 17
		self.rect.centerx = self.pos.x
		self.rect.centery = self.pos.y

class Missile(Bullet):
	def __init__(self, position, speed, angle, uid, wing, spritesheet):
		super().__init__(position, speed, angle, uid, wing, spritesheet)
		self.type = "missile"
		self.pos = Vector2D(position.centerx, position.centery)
		self.target = Vector2D(SCREEN_X/2, SCREEN_Y/2)
		self.spriterect = SUPER_BULLET
		self.new_sprite(self.spriterect)
		self.maxspeed = 10

	def update(self):
		self.calc_angle()
		self.speed_limit()
		self.new_sprite(self.spriterect) #Rotate image

		distance = (self.pos - self.target).magnitude()
		f = (300 * 100) / (distance ** 2)

		gravity_direction = Vector2D((self.target.x - self.pos.x),(self.target.y - self.pos.y)).normalized()
		gravity_force = gravity_direction * f
		self.speed += gravity_force

		self.pos += self.speed
		self.rect.center = (self.pos.x, self.pos.y)

	def update_target(self, pos):
		self.target = pos
		print ("Got target")