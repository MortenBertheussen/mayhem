#!/usr/bin/env python3
from gameconstants import *
from Vector2D import *
from spritesheet import *
import math

RESPAWN_TIMER = pygame.USEREVENT + 2

class Movingobject(pygame.sprite.Sprite):
	"""A class for movingobjects"""
	def __init__(self):
		super().__init__()
		self.pos = Vector2D(SCREEN_X/2 - 22, SCREEN_Y/2 - 22)
		self.speed = Vector2D(0,-1)
		self.angle = 0
		self.maxspeed = 5

	def screen_wrap(self):
		"""Make moving objects wrap around if they go out of the screen"""
		if self.pos.x <= 0: 		self.pos.x = SCREEN_X - 1	#Left
		if self.pos.x >= SCREEN_X:	self.pos.x = 1				#Right
		if self.pos.y >= SCREEN_Y:	self.pos.y = 1				#Bottom
		if self.pos.y <= 0:			self.pos.y = SCREEN_Y - 1 	#Top

	def rotate(self):
		"""The math behind finding the new direction with an angle"""
		x = self.speed.x * math.cos(math.radians(-self.angle)) - self.speed.y * math.sin(math.radians(-self.angle))
		y = self.speed.x * math.sin(math.radians(-self.angle)) + self.speed.y * math.cos(math.radians(-self.angle))
		return new_speed

	def rotate_point(self, point, center, angle):
		ang = math.radians(-angle)
		x1 = point.x - center.x
		y1 = point.y - center.y
		x2 = x1 * math.cos(ang) - y1 * math.sin(ang)
		y2 = x1 * math.sin(ang) + y1 * math.cos(ang)
		pointx = x2 + center.x
		pointy = y2 + center.y

		return Vector2D(pointx,pointy)

	def new_sprite(self, rect):
		"""Fetches a new sprite from the spritesheet and keep its rotation"""
		oldrect = self.rect
		self.image = self.spritesheet.get_image(rect)
		self.image = pygame.transform.rotate(self.image, self.angle)
		self.rect = self.image.get_rect(center=oldrect.center)

	def rotate_left(self):
		x = self.speed.x * math.cos(math.radians(-4)) - self.speed.y * math.sin(math.radians(-4))
		y = self.speed.x * math.sin(math.radians(-4)) + self.speed.y * math.cos(math.radians(-4))
		self.speed = Vector2D(x, y)
		self.calc_angle()

	def rotate_right(self):
		x = self.speed.x * math.cos(math.radians(4)) - self.speed.y * math.sin(math.radians(4))
		y = self.speed.x * math.sin(math.radians(4)) + self.speed.y * math.cos(math.radians(4))
		self.speed = Vector2D(x, y)
		self.calc_angle()

	def calc_angle(self):
		baseline = Vector2D(0,-1) #Vector pointing upwards
		dot = (self.speed.x * baseline.x) + (self.speed.y * baseline.y)
		det = (self.speed.x * baseline.y) - (self.speed.y * baseline.x)
		angle = math.atan2(det, dot)
		self.angle = math.degrees(angle)

	def speed_limit(self):
		"""Speed_limit method of rocket"""
		if self.speed.magnitude() > self.maxspeed:
			self.speed = self.speed.normalized() * self.maxspeed