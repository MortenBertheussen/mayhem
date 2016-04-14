#!/usr/bin/env python3
from config import *
from gameconstants import *
from Vector2D import *
from spritesheet import *
from movingobject import *
import math
import random

class Astroid(Movingobject):
	"""This is the astroid class"""
	def __init__(self, spawn, rect, spritesheet):
		super().__init__(0, spritesheet, spawn)
		self.speed = Vector2D(random.choice([-3, -2, -1, 1, 2, 3]), random.choice([-3, -2, -1, 1, 2, 3]))
		self.image = self.spritesheet.get_image((rect))
		self.image_pos = rect
		self.rect = self.image.get_rect()
		self.angle = 0
		self.spin = random.uniform(0,5)
		self.maxspeed = 3
		if rect is ASTROID_1:
			self.mass = ASTROID_BIG_MASS
			self.type = 1
			self.life = 3
		if rect is ASTROID_2:
			self.mass = ASTROID_MEDIUM_MASS
			self.type = 2
			self.life = 2
		if rect is ASTROID_3:
			self.mass = ASTROID_SMALL_MASS
			self.type = 3
			self.life = 1
	
	def screen_wrap(self):
		"""Custom screenwrap for astroids"""
		if self.pos.x <= -100: 				self.pos.x = SCREEN_X + 50				#Left
		if self.pos.x >= SCREEN_X + 100:	self.pos.x = -50						#Right
		if self.pos.y >= SCREEN_Y + 100:	self.pos.y = -50						#Bottom
		if self.pos.y <= -100:				self.pos.y = SCREEN_Y + 50 				#Top

	def update(self):
		"""Runs what is needed for the class"""
		self.angle += self.spin
		self.new_sprite(self.image_pos)
		self.move()
		self.speed_limit()
		self.screen_wrap()

	def move(self):
		"""Controls the movement of the astroid"""
		self.pos += self.speed
		self.rect.centerx = self.pos.x
		self.rect.centery = self.pos.y

	def new_sprite(self, rect):
		"""Fetches a new sprite from the spritesheet and keep its rotation"""
		oldrect = self.rect
		self.image = self.spritesheet.get_image(rect)
		self.image = pygame.transform.rotate(self.image, self.angle)
		self.rect = self.image.get_rect(center=oldrect.center)