#!/usr/bin/env python3
from gameconstants import *
from Vector2D import *
from spritesheet import *
from movingobject import *
import math

class Bullet(Movingobject):
	"""The bullet class"""
	def __init__(self, uid, spritesheet, spawn, speed, angle, wing):
		super().__init__(uid, spritesheet, spawn, speed)
		if uid is 1:	self.image = self.spritesheet.get_image(RED_LASER)
		else:			self.image = self.spritesheet.get_image(BLUE_LASER)
		self.rect = self.image.get_rect()
		self.type = "bullet"
		self.angle = angle
		if uid is 1:	self.new_sprite(RED_LASER)
		else:			self.new_sprite(BLUE_LASER)

		if wing is "left":
			point = Vector2D(self.pos.x-7, self.pos.y-10)
			self.pos = self.rotate_point(point, self.pos, self.angle)
		else:
			point = Vector2D(self.pos.x+7, self.pos.y-10)
			self.pos = self.rotate_point(point, self.pos, self.angle)
		

	def update(self):
		"""Runs what is needed for the class"""
		self.pos += self.speed.normalized() * 17
		self.rect.centerx = self.pos.x
		self.rect.centery = self.pos.y

class Missile(Movingobject):
	def __init__(self, uid, spritesheet, spawn, speed, angle, wing):
		super().__init__(uid, spritesheet, spawn, speed)
		self.speed = speed.normalized()
		self.image = self.spritesheet.get_image(RED_LASER)
		self.rect = self.image.get_rect()
		self.type = "missile"
		self.target = self.pos #No target to begin with
		self.angle = angle
		self.new_sprite(SUPER_BULLET)
		self.maxspeed = 10

		if wing is "left":
			point = Vector2D(self.pos.x-20, self.pos.y-10)
			self.pos = self.rotate_point(point, self.pos, self.angle)
		else:
			point = Vector2D(self.pos.x+20, self.pos.y-10)
			self.pos = self.rotate_point(point, self.pos, self.angle)

	def update(self):
		self.calc_angle()
		self.speed_limit()
		self.new_sprite(SUPER_BULLET) #Rotate image

		distance = (self.pos - self.target).magnitude()
		f = (300 * 100) / (distance ** 2)

		gravity_direction = Vector2D((self.target.x - self.pos.x),(self.target.y - self.pos.y)).normalized()
		gravity_force = gravity_direction * f
		self.speed += gravity_force

		self.pos += self.speed
		self.rect.center = (self.pos.x, self.pos.y)

	def update_target(self, pos):
		self.target = pos